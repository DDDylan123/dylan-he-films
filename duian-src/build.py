"""《对岸》互动原型构建脚本（剧本 v2）。

用法（在 duian-src/ 里运行）：
  python3 build.py                 # 媒体从同目录的 ../duian/m/ 读取（本地试玩）
  python3 build.py <CDN 前缀>       # 媒体走 CDN，失败再退回 GitHub Pages；见 deploy.sh

产物直接写到 ../duian/index.html。
媒体编号固定记在 media_map.json：已有的文件永不改号，新文件从 new/ 或 media_lite/ 里找，复制进 ../duian/m/ 并取下一个编号。
同时生成 配音清单.txt：所有还没有配音的台词。
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'duian')
SRCS = [os.path.join(HERE, d) for d in ('new', 'media_lite')]
MAP_PATH = os.path.join(HERE, 'media_map.json')
media_map = json.load(open(MAP_PATH, encoding='utf-8'))
used = set()


def M(name):
    """Media filename -> stable short published path (m/NN.ext)."""
    if name not in media_map:
        src = next((os.path.join(d, name) for d in SRCS if os.path.exists(os.path.join(d, name))), None)
        assert src, f'缺素材：{name}（放进 duian-src/new/）'
        nums = [int(os.path.basename(v).split('.')[0]) for v in media_map.values()]
        short = f'm/{max(nums) + 1:02d}{os.path.splitext(name)[1]}'
        shutil.copy(src, os.path.join(OUT, short))
        media_map[name] = short
    assert os.path.exists(os.path.join(OUT, media_map[name])), media_map[name]
    used.add(name)
    return media_map[name]


def shot(s, sub, en, who, line, vo, need, **kw):
    """sub = 普通话字幕；line = 实际要说的原话（沪语写法），没有 vo 时自动记进配音清单。"""
    s.update(sub=sub, en=en)
    if who: s['who'] = who
    if line: s['line'] = line
    if vo: s['vo'] = M(vo)
    needs = [need] if need else []
    if line and not vo:
        needs.append(f'待配音·{who or "旁白"}')
    if needs: s['need'] = '；'.join(needs)
    for k, v in kw.items():
        if v is not None: s[k] = v
    return s


def img(n, sub='', en='', who=None, line=None, vo=None, need=None, dur=4.5, **kw):
    return shot({'t': 'img', 'src': M(f'img_{n}.webp'), 'dur': dur}, sub, en, who, line, vo, need, **kw)


def vid(n, sub='', en='', who=None, line=None, vo=None, need=None, **kw):
    return shot({'t': 'vid', 'src': M(f'vid_{n}.mp4')}, sub, en, who, line, vo, need, **kw)


def ph(desc, sub='', en='', who=None, line=None, vo=None, need='待补静帧', dur=4.5, **kw):
    """Placeholder still: not yet generated."""
    return shot({'t': 'ph', 'desc': desc, 'dur': dur}, sub, en, who, line, vo, need, **kw)


def card(text, en='', dur=5, **kw):
    """黑底白字卡：题记、题词卡。"""
    s = {'t': 'card', 'text': text, 'en': en, 'dur': dur}
    s.update({k: v for k, v in kw.items() if v is not None})
    return s


def V(line, sub=None, en=''):
    """旁白（老年阿乔，市区话）。sub 省略时字幕与原话相同。"""
    return dict(who='旁白', line=line, sub=sub or line, en=en)


def met(then, other=None):
    s = {'if': 'met', 'then': then}
    if other: s['else'] = other
    return s


WALTZ = 'aud_MUS_主题_大提琴华尔兹.mp3'
ACC = 'aud_MUSIC_对岸主题_v1.mp3'
JAZZ = 'aud_MUS_饭局现场_老上海爵士.mp3'
VO_AYI = 'aud_阿姨_上海话_v4a.mp3'
PD_EAT = 'aud_PD_老金_吃仔饭再去_a.mp3'
PD_FIX = 'aud_PD_老金_修修还好用格_a.mp3'
PD_MATCH = 'aud_PD_老金_夜里冷迭盒自来火拿去_b.mp3'
PD_THERE = 'aud_PD_老金_依bebe有啥好_a.mp3'
VO_S24 = 'aud_VO_S24口型版音轨_父女.mp3'

K_LADY = '2016，浦西老太太立在阿乔出租房的窗口（他的母亲）'

# 2026-10-08 Dylan 选定的 v2 静帧（LibTV 节点 V2_*，Seedream 5.0 Pro）
I_TABLE = 'KF_V2_01_1991灶间两只碗_b'
I_TYRE = 'KF_V2_02_1991修车摊补胎_b'
I_MATCH = 'KF_V2_03_1991灶头塞火柴_a'
I_BACK = 'KF_V2_04_1991她转身借火背影_a'
I_DOOR = 'KF_V2_05_1992老张老金门口_a'
I_NEWFLAT = 'KF_V2_06b_1994新村钥匙_新房_实景光_a'
I_ZHOU = 'KF_V2_07b_1996周敏敲门_实景光_a'
I_ROOM = 'KF_V2_08_1996浦西亭子间_b'
I_WALKOUT = 'KF_V2_09b_1995走出饭店外滩夜风_b'
I_BOX = 'KF_V2_10b_1995火柴盒落江_b'
I_PIER = 'KF_V2_11b_1995码头末班轮渡_a'
I_JIN = 'KF_V2_14_2016老金老阿乔灶间修车_a'
I_CURTAIN = 'KF_V2_15_2016拉窗帘_b'
I_STOVE = 'KF_V2_16_空火柴盒放回灶头_b'

nodes = {
 'prologue': {'year': '2016', 'music': WALTZ, 'shots': [
    card('一九九〇年，浦东开发。\n在那以前，上海人讲：宁要浦西一张床，不要浦东一间房。',
         '1990: Pudong opens for development. Before that, Shanghai people said:\n“Better a bed in Puxi than a flat in Pudong.”', dur=6),
    vid('VID_N1_老阿乔火柴_Kling3', **V('江两边个灯，我数了廿五年。', '江两边的灯，我数了二十五年。',
        'The lights on both banks — I counted them for twenty-five years.')),
    vid('VN2_火柴盒满', **V('一九九一年三月，夜里向九点钟。浦东个灯，一盏一盏，数得清。',
        '一九九一年三月，晚上九点。浦东的灯，一盏一盏，数得清。',
        'March 1991, nine at night. The lights of Pudong — you could still count them, one by one.'), year='1991'),
   ], 'next': 'k1'},

 'k1': {'year': '1991', 'music': WALTZ, 'shots': [
    img(I_TABLE, '吃了饭再走，外面风大得很。', 'Eat first, then go. The wind’s fierce out there.',
       who='老金', line='吃仔饭再去，外头 hong 大来邪。', vo=PD_EAT),
    img(I_TABLE, **V('老金是我师傅。我十六岁起跟伊过，跟伊学修脚踏车。', '老金是我师傅。我十六岁起跟着他过，跟他学修自行车。',
       'Lao Jin was my master. From sixteen I lived with him and learned to fix bicycles.')),
    img(I_TABLE, **V('爷跟厂里支内，去了外地。姆妈不肯去，过江回了娘家。', '我爸跟着厂里支内，去了外地。我妈不肯去，过江回了娘家。',
       'My father went inland with his factory. My mother wouldn’t go; she crossed the river, back to her family.')),
    img(I_TABLE, **V('临走讲，过两个号头来接我。屋里个平房留拨我，就辣老金隔壁。', '走的时候说，过两个月来接我。家里的平房留给了我，就在老金隔壁。',
       'She said she’d come for me in two months. They left me the house, right next door to Lao Jin.')),
    img(I_TABLE, **V('我等到今朝。', '我等到今天。', 'I’m still waiting.'), dur=3.5),
    img(I_TYRE, '修修还能用的。', 'Patch it up. It still works.',
       who='老金', line='修修还好用格。', vo=PD_FIX),
    img(I_MATCH, '夜里冷，这盒火柴拿去。', 'It’s cold at night. Take these matches.',
       who='老金', line='夜里冷，迭盒自来火拿去。', vo=PD_MATCH, box=True),
    img(I_MATCH, **V('伊不晓得，我每夜跑到江边，是去数对岸个灯。', '他不知道，我每天晚上跑到江边，是去数对岸的灯。',
       'He didn’t know that every night I went down to the river to count the lights on the other side.')),
   ], 'next': 'c1'},

 'c1': {'year': '1991', 'music': WALTZ, 'shots': [
    img('KF_P1_码头全景_她走来', **V('末班轮渡前，一个浦西女人走过来。', en='Before the last ferry, a woman from Puxi walked over.')),
    img('KF_P2_她举烟借火', '有火吗？', '“Got a light?”', who='薇薇', line='有火伐？'),
   ], 'choice': {'q': '火一亮，你看得见她；她也看得见你。', 'qen': 'Strike a light and you will see her — and she will see you.', 'opts': [
      {'l': '划一根自来火', 'en': 'Strike a match', 'to': 'n1a', 'set': 'met', 'burn': 1},
      {'l': '讲：呒没', 'en': '“I don’t have one.”', 'to': 'n1b'}]}},

 'n1a': {'year': '1991', 'music': WALTZ, 'shots': [
    img('KF_W1_薇薇定妆_借火特写', **V('我借拨伊一根自来火。', '我借给她一根火柴。', 'I gave her a match.')),
    img('KF_P5_他在火光里看她', **V('火光里，我第一趟看清爽伊个面孔。', '火光里，我第一次看清她的脸。', 'In the flare, I saw her face clearly for the first time.')),
    img('KF_P6_她在轮渡雨窗后', **V('伊上了船。', '她上了船。', 'She got on the boat.')),
    vid('VID_S18_Kling3', **V('从此以后，对岸有了一个人。', '从那以后，对岸有了一个人。', 'From then on, there was someone on the other shore.')),
   ], 'next': 'c2'},

 'n1b': {'year': '1991', 'music': WALTZ, 'shots': [
    img(I_BACK, **V('我讲，呒没。', '我说，没有。', '“No,” I said.')),
    img(I_BACK, **V('自来火辣我袋袋里，一根也没少。', '火柴在我口袋里，一根也没少。', 'The matches stayed in my pocket. Not one missing.')),
    vid('VID_S09_Kling3', **V('对岸，还是对岸。', en='The other shore was still the other shore.')),
   ], 'next': 'c2'},

 'c2': {'year': '1992', 'music': ACC, 'shots': [
    vid('VID_S03_Kling3', **V('一九九二年，动迁个消息来了。江上头已经有了桥，人心里向个江，还没。',
        '一九九二年，动迁的消息来了。江上已经有了桥，人心里的江，还没有。',
        '1992. Word of the demolitions came. There was a bridge over the river now — but not over the one in people’s heads.')),
    vid('VID_S05_口型_v2', '量到哪里，算到哪里。', '“Whatever we measure is what you get.”', who='老张（公事，市区腔）'),
    img('KF_S09w_晾衣望对岸', **V('一夜之间，隔壁人家个屋顶上，长出了楼。', '一夜之间，隔壁人家的屋顶上，长出了楼。',
        'Overnight, extra floors sprouted on the neighbours’ roofs.')),
    img(I_DOOR, '老金，你也加一层，不加吃亏的。', '“Lao Jin, add a floor too. You lose out if you don’t.”',
       who='老张（私下，浦东话）', line='老金，侬也加一层，弗加吃亏格。', need='浦东话生成中（L7）'),
    img(I_DOOR, '不是我们的，拿了夜里睡不着。', '“It isn’t ours. Take it and you won’t sleep at night.”',
       who='老金', line='弗是吾伲格，拿仔夜里困弗着。', need='浦东话待生成（L5，写作“五泥”）'),
    img(I_DOOR, '你加吗？', '“Are you adding one?”', who='老金（转向阿乔）', line='侬加伐？', need='浦东话待选（L6）', dur=3.5),
   ], 'choice': {'q': '多一层，多一套房。也多一夜困弗着。', 'qen': 'One more floor, one more flat. And one more sleepless night.', 'opts': [
      {'l': '加，连夜加楼', 'en': 'Build, tonight', 'to': 'n2a'},
      {'l': '勿加，跟老金一样', 'en': 'Don’t, like Lao Jin', 'to': 'n2b'}]}},

 'n2a': {'year': '1992–1994', 'music': ACC, 'shots': [
    vid('VID_S07_Kling3', '加。', '“Build.”', who='年轻阿乔（浦东话）', line='加。', need='浦东话待生成（L8）'),
    vid('VID_S08_Kling3', '老板，三层要加钢筋，不然要塌的。', '“Boss, three floors needs rebar, or it’ll come down.”',
        who='小陈（苏北口音普通话）', line='老板，三层要加钢筋，不然要塌的。'),
    vid('VID_S10_Kling3', **V('两年里向，我加了三层。楼是假个，钢筋是真个。', '两年里，我加了三层。楼是假的，钢筋是真的。',
        'In two years I added three floors. The floors were fake. The rebar was real.')),
    vid('VID_S11_Seedance2_0'),
    vid('VID_S14_Kling3', **V('老屋拆脱，分到四套新房子。', '老房子拆了，分到四套新房子。', 'The old house came down. I got four new flats.')),
   ], 'next': 'c3'},

 'n2b': {'year': '1994', 'music': WALTZ, 'shots': [
    vid('VID_S13_Kling3', **V('我跟老金一样，一层也没加。', en='Like Lao Jin, I didn’t add a single floor.')),
    img(I_NEWFLAT, **V('一九九四年，搬进新村。一套，新个。', '一九九四年，搬进新村。一套，新的。', '1994. We moved into the new estate. One flat. Brand new.')),
    vid('VID_S22_Kling3', **V('隔壁就是老金。我屋里没装灶，夜饭还是搭伊吃。', '隔壁就是老金。我家没装灶，晚饭还是跟他一起吃。',
        'Lao Jin was next door. I never put in a stove; I still ate dinner at his.')),
   ], 'next': 'c5'},

 'c3': {'year': '1994', 'music': WALTZ, 'shots': [
    img('KF_N6_final', **V('四把钥匙。每一把，都开一扇浦东个门。', '四把钥匙。每一把，都开一扇浦东的门。', 'Four keys. Every one of them opened a door in Pudong.')),
    img('KF_S09_final', **V('哪能还是浦东。', '怎么还是浦东。', 'And still — Pudong.'), dur=3.5),
    img('KF_S22_老金炒菜', '那边有什么好？', '“What’s so good over there?”', who='老金', line='依 be be 有啥好？', vo=PD_THERE),
   ], 'choice': {'q': '四扇门，都在你身后。', 'qen': 'Four doors, all of them behind you.', 'opts': [
      {'l': '统统卖脱，过江', 'en': 'Sell them all, cross the river', 'to': 'n3a'},
      {'l': '留在浦东', 'en': 'Stay in Pudong', 'to': 'e3'}]}},

 'n3a': {'year': '1995', 'music': WALTZ, 'shots': [
    vid('VID_S15_Kling3_v3', **V('我一日也没住过，夜里还是困辣老金屋里。统统卖脱，去买了浦西。',
        '我一天也没住过，晚上还是睡在老金家。全部卖掉，去买了浦西。',
        'I never spent a night in them — I still slept at Lao Jin’s. I sold the lot and bought in Puxi.')),
    vid('VID_S15c_Kling3', **V('四套房子，换一间弄堂里个老公寓。', '四套房子，换了弄堂里一间老公寓。', 'Four flats, for one old apartment down a Puxi lane.')),
    img('KF_Q1_新房窗口望对面', dur=3.5),
    met(img('KF_Q2_对面窗里是她', **V('我花了四年，走到伊对面。', '我花了四年，走到她对面。', 'It took me four years to end up across from her.')),
        img('KF_Q2_对面窗里是她', **V('对面窗里，是一户浦西人家。窗帘是丝绒个。', '对面窗里，是一户浦西人家。窗帘是丝绒的。',
            'In the window opposite, a Puxi family. Velvet curtains.'))),
   ], 'next': 'c4'},

 'c4': {'year': '1995', 'year_if': ['sold', '1996'], 'music': JAZZ, 'shots': [
    img('KF_B1_饭局全景', **V('卖房子拨我个沈先生，请新邻居吃饭。', '卖房子给我的沈先生，请新邻居吃饭。',
        'Mr Shen, who had sold me the flat, invited his new neighbour to dinner.')),
    met(img('KF_B2_她近景_吊灯光', **V('火柴换成了吊灯。是伊。', '火柴换成了吊灯。是她。', 'The match had become a chandelier. It was her.')),
        img('KF_B2_她近景_吊灯光', **V('伊是沈家个女主人。', '她是沈家的女主人。', 'She was the lady of the Shen house.'))),
    img('KF_B5_打火机先点', **V('伊拿出一根香烟。我个手，比我个脑子先动。', '她拿出一根香烟。我的手，比我的脑子先动。',
        'She took out a cigarette. My hand moved before my head did.')),
    img('KF_B5_打火机先点', **V('沈先生个打火机，先点着了。', '沈先生的打火机，先点着了。', 'Mr Shen’s lighter got there first.'), dur=3.5),
    img('KF_B7_耳语_阿乔视角', '你原来是哪里人？', '“Where are you from, originally?”', who='沈家骏', line='侬老底子是阿里人？', dur=3.5),
    img('KF_B7_耳语_阿乔视角', '……浦东。', '“…Pudong.”', who='阿乔', line='……浦东。', dur=3),
    img('KF_B7_耳语_阿乔视角', '浦东啊？乡下呀。', '“Pudong? That’s the countryside.”', who='薇薇（侧身对丈夫，轻声）',
        line='浦东啊？乡下头呀。', vo=VO_AYI, need='现在是旧的阿姨声音，要用薇薇的声音重配'),
    img('KF_B8_阿乔僵住的笑', dur=3.5),
   ], 'choice': {'q': '一桌子人都在笑。你也可以笑。', 'qen': 'The whole table is laughing. You could laugh too.', 'opts': [
      {'l': '笑笑，坐下去', 'en': 'Smile, sit back down', 'to': 'e1'},
      {'l': '起身，走出去', 'en': 'Stand up and leave', 'to': 'e2'}]}},

 'c5': {'year': '1996', 'music': WALTZ, 'shots': [
    img(I_ZHOU, '乔师傅，沈先生托我来的。这套房子，你开个价。', '“Master Qiao — Mr Shen sent me. Name your price for the flat.”',
       who='周敏', line='乔师傅，沈先生托我来个。迭套房子，侬开个价。'),
    img(I_ZHOU, **V('一九九六年，浦东涨了。涨得还不够多，正好够我动心。', '一九九六年，浦东涨了。涨得还不够多，刚好够我动心。',
       '1996. Pudong had gone up. Not by enough — just enough to tempt me.')),
   ], 'choice': {'q': '这笔钱，够买浦西一间亭子间。不够买回一个灶间。', 'qen': 'Enough for a box room in Puxi. Not enough to buy back a kitchen.', 'opts': [
      {'l': '卖掉，买间亭子间', 'en': 'Sell, buy a box room in Puxi', 'to': 'n5a', 'set': 'sold'},
      {'l': '勿卖', 'en': 'Keep it', 'to': 'e4'}]}},

 'n5a': {'year': '1996', 'music': WALTZ, 'shots': [
    img(I_ROOM, **V('钞票只够一间亭子间，朝北，冬天晒不着太阳。', '钱只够一间亭子间，朝北，冬天晒不到太阳。',
       'The money bought a box room facing north. No sun in winter.')),
    img(I_ROOM, **V('卖拨我亭子间个，也是迭位沈先生。伊请我吃饭。', '卖亭子间给我的，也是这位沈先生。他请我吃饭。',
       'The man who sold it to me was that same Mr Shen. He invited me to dinner.')),
   ], 'next': 'c4'},

 'e1': {'year': '1999', 'music': WALTZ, 'ending': 1, 'shots': [
    img('KF_Q1_新房窗口望对面', **V('过江以后，我搭老金，一年只吃一顿年夜饭。后来，年夜饭也没了。',
        '过江以后，我跟老金一年只吃一顿年夜饭。后来，年夜饭也没了。',
        'After I crossed, Lao Jin and I ate together once a year, on New Year’s Eve. Then not even that.')),
    met(img('KF_V1v2_1999沈家擦肩_b', **V('一九九九年，外滩。伊走过我身边，回头看了一眼。火一熄，伊就转回去了。',
            '一九九九年，外滩。她走过我身边，回头看了一眼。火一灭，她就转回去了。',
            '1999, the Bund. She passed me and glanced back. When the flame died, she turned away.'), dur=5.5),
        img('KF_V1v2_1999沈家擦肩_b', **V('一九九九年，外滩。沈家一家门走过我身边。沈太太看了我一眼，没认出我。',
            '一九九九年，外滩。沈家一家人走过我身边。沈太太看了我一眼，没认出我。',
            '1999, the Bund. The Shens walked past me. Mrs Shen looked at me and didn’t know me.'), dur=5.5)),
    img('KF_S24v2_1999沈家父女_b', '「爸爸，对面是什么地方？」「浦东。」', '“Daddy, what’s over there?” “Pudong.”',
        who='沈囡囡 / 沈家骏', line='阿爸，对面是啥地方？ / 浦东。', vo=VO_S24,
        need='暂用旧 S24 口型版音轨，父亲要换成沈家骏的声音'),
    vid('VN3_火柴剩三根', **V('浦东个灯，我数不清了。自来火，还剩三根。', '浦东的灯，我数不清了。火柴，还剩三根。',
        'I could no longer count the lights of Pudong. Three matches left.'), left=3),
    vid('VID_S28_Kling3', year='2016'),
    vid('VID_S29_Seedance2_0_1080p', **V('二〇一六年，我划最后一根。', '二〇一六年，我划了最后一根。', '2016. I struck the last one.'), left=0, sfx='strike'),
    vid('VID_S26_Kling3_v3', **V('对岸个灯，我看了一世人生。呒没一盏，是为我亮个。', '对岸的灯，我看了一辈子。没有一盏，是为我亮的。',
        'I watched the lights on the other shore all my life. Not one of them was lit for me.')),
    vid('VN4_老金厨房2016'),
    vid('VN5_对岸远窗2016', **V('……有一盏，辣楼背后。我看了一世人生，一趟也没看见。', '……有一盏，在楼背后。我看了一辈子，一次也没看见。',
        '…There was one, behind the towers. I looked all my life and never once saw it.'),
        need='反打要是全片唯一一个不动的镜头，考虑换成静帧'),
    card('人望了一辈子对岸。对岸也在望，望个是另一个对岸。', 'We spend our lives looking at the other shore. The other shore is looking too — at another shore.'),
   ]},

 'e2': {'year': '1995', 'year_if': ['sold', '1996'], 'music': WALTZ, 'ending': 2, 'shots': [
    img(I_WALKOUT, **V('我放下筷子。没人留我。', en='I put down my chopsticks. No one asked me to stay.')),
    img('KF_S23_外滩人群', **V('外滩个风，比浦东大。', '外滩的风，比浦东大。', 'The wind on the Bund was stronger than in Pudong.')),
    img(I_BOX, **V('我把自来火盒子掼进黄浦江。伊漂了一歇，没沉。', '我把火柴盒扔进黄浦江。它漂了一会儿，没沉。',
       'I threw the matchbox into the Huangpu. It floated a while. It didn’t sink.'), box=False),
    img(I_BOX, **V('我掼脱个，是老金个自来火。', '我扔掉的，是老金的火柴。', 'What I threw away were Lao Jin’s matches.')),
    img(I_PIER, **V('浦东个房子卖脱了，浦西个门开弗进。', '浦东的房子卖掉了，浦西的门进不去。',
       'The Pudong flats were sold. The doors of Puxi wouldn’t open to me.')),
    img(I_PIER, **V('末班轮渡辣叫。我立辣码头上，没上船，也没走。', '末班轮渡在鸣笛。我站在码头上，没上船，也没走。',
       'The last ferry sounded its horn. I stood on the pier. I didn’t board. I didn’t leave.')),
    img(I_PIER, **V('一条江，过得去，就回弗来；回得来，就过弗去。', '一条江，过得去，就回不来；回得来，就过不去。',
       'A river: cross it and you can’t come back; come back and you can’t cross.')),
    card('人一生最远个路，是半条江。', 'The longest road in a life is half a river.'),
   ]},

 'e3': {'year': '1994–2016', 'music': WALTZ, 'ending': 3, 'shots': [
    vid('VID_S12_Seedance2_0', **V('我留了下来。', en='I stayed.')),
    vid('VID_S28_Kling3', **V('浦东起来了。四套房子，我收了一世人生个房租。', '浦东起来了。四套房子，我收了一辈子房租。',
        'Pudong rose. Four flats — I collected rent on them all my life.')),
    img('KF_N4b_2016老金厨房窗', **V('老金就住辣隔开两条马路个新村里。我一年去看伊一趟。', '老金就住在隔两条马路的新村里。我一年去看他一次。',
        'Lao Jin lived in the estate two streets away. I went to see him once a year.')),
    ph('2016，老阿乔在浦东三十八楼窗前，望浦西', **V('二〇一六年，我立辣三十八楼，终于比对岸高了。', '二〇一六年，我站在三十八楼，终于比对岸高了。',
       '2016. Thirty-eight floors up, I was finally higher than the other shore.'), year='2016'),
    ph('周敏领一位浦西老太太来看房', **V('有一日，周敏领一个浦西老太太来租我个房子。伊老屋动迁了，要搬到浦东来。',
       '有一天，周敏领着一位浦西老太太来租我的房子。她的老房子动迁了，要搬到浦东来。',
       'One day Zhou Min brought an old lady from Puxi to rent one of my flats. Her old house was being torn down; she was moving to Pudong.'), dur=5.5),
    ph(K_LADY, '浦东现在挺好的。', '“Pudong’s quite nice now.”', who='老太太（市区话）', line='浦东现在蛮好。', dur=3.5),
    ph(K_LADY, **V('我认得伊。伊不认得我。', '我认得她。她不认得我。', 'I knew her. She didn’t know me.')),
    ph(K_LADY, **V('我收了伊三个号头押金。我没叫伊姆妈。', '我收了她三个月押金。我没叫她妈。', 'I took three months’ deposit. I didn’t call her Mum.')),
    ph(K_LADY, **V('我一直以为，对岸是一个地方。', en='All along, I thought the other shore was a place.')),
    card('立得再高，也看不见自家身后。', 'However high you stand, you can’t see what’s behind you.'),
   ]},

 'e4': {'year': '2016', 'music': WALTZ, 'ending': 4, 'shots': [
    img('KF_N4b_2016老金厨房窗', **V('二十年。新村住旧了。', en='Twenty years. The new estate grew old.')),
    vid('VN4_老金厨房2016', **V('浦东个房子涨到天上，我个只涨了一点点。人家讲我戆。', '浦东的房子涨到天上，我的只涨了一点点。人家说我傻。',
        'Pudong prices went sky-high. Mine went up a little. People called me a fool.')),
    img(I_JIN, '修修还能用的。', 'Patch it up. It still works.', who='老金（老了）', line='修修还好用格。', vo=PD_FIX,
       need='暂用中年老金的声音，老年版待生成'),
    img(I_JIN, **V('伊讲个是脚踏车。我晓得，伊讲个是人。', '他说的是自行车。我知道，他说的是人。', 'He meant the bicycle. I knew he meant me.')),
    met(img(I_CURTAIN, dur=3.5)),
    ph('灶间窗口，窗外是陆家嘴的背影', **V('我一世人生没过江。对岸个灯是啥样子，我只看过。', '我一辈子没过江。对岸的灯是什么样子，我只看过。',
       'I never crossed the river in my life. The lights over there — I only ever looked at them.')),
    img(I_STOVE, dur=3.5, box=False),
    img(I_STOVE, **V('二〇一六年冬天，老金走了。', en='In the winter of 2016, Lao Jin died.')),
    img('KF_N4b_2016老金厨房窗', **V('灶间个灯，换我来开。不晓得为啥人开。', '灶间的灯，换我来开。不知道为谁开。',
        'Now I keep the kitchen light on. I don’t know who for.')),
    card('有人一辈子去对岸点灯，有人一辈子在身后守灯。', 'Some spend their lives lighting lamps on the other shore. Some spend theirs keeping one lit behind them.'),
   ]},

 # 隐藏结局《灯》：四个结局都看过后，标题页多出一根火柴。全剧唯一一次老金自己开口（只出字幕：浦东话写法 + 普通话）。
 'lamp': {'year': '1991–2016', 'music': None, 'ending': 5, 'shots': [
    card('', dur=2, sfx='strike', box=False),
    # 同一扇窗：1994（S22）→ 1999 → 2005 → 2010 → 2016（N4b），一张叠一张
    img('KF_S22_老金炒菜', '一九九一年到二〇一六年，灶间个灯，夜夜开到天亮。', 'From 1991 to 2016, the kitchen light stayed on every night till dawn.',
        mid='一九九一年到二〇一六年，灶间的灯，每天晚上开到天亮。', dur=5.5),
    img('KF_V2_18_灯_1999同一扇窗_b', '电费单上，一个号头多七八角洋钿。', 'Seven or eight jiao more on the electricity bill, every month.',
        mid='电费单上，一个月多七八毛钱。', dur=5),
    img('KF_V2_19_灯_2005同一扇窗_a', '伊走了四条路。', 'He walked four roads.', mid='他走了四条路。', dur=4),
    img('KF_V2_20_灯_2010同一扇窗_b', '四条路上，我一夜也没关。', 'On every one of them, I never turned it off. Not one night.',
        mid='四条路上，我一夜也没关。', dur=5),
    img('KF_N4b_2016老金厨房窗', dur=4),
    card('', dur=2),
   ]},
}

endings = {
 1: {'name': '对岸', 'en': 'The Other Shore', 'line': '他得到了对岸，对岸没有得到他。'},
 2: {'name': '掼脱', 'en': 'Let Go', 'line': '他保住了自己，却把两岸都弄丢了。'},
 3: {'name': '赢家', 'en': 'The Winner', 'line': '他赢了这个时代。对岸终于自己走到他面前，他却开不了口。'},
 4: {'name': '老金的窗', 'en': 'Lao Jin’s Window', 'line': '他少拿了三套房，一辈子没过江，最后连守灯的人也失去了。'},
 5: {'name': '灯', 'en': 'The Lamp', 'line': ''},
}

for n in nodes.values():
    if n.get('music'): n['music'] = M(n['music'])

story = {'start': 'prologue', 'nodes': nodes, 'endings': endings, 'matches': 12}
base = sys.argv[1] if len(sys.argv) > 1 else ''
tpl = open(os.path.join(HERE, 'index.tpl.html'), encoding='utf-8').read()
body = tpl.replace('/*STORY*/null', json.dumps(story, ensure_ascii=False)).replace("/*BASE*/''", json.dumps(base))
head = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex">\n')
body = body.replace('</style>', '</style>\n</head>\n<body>', 1)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')
json.dump(media_map, open(MAP_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 配音清单：所有还没有配音的台词，按出场顺序
order = ['prologue', 'k1', 'c1', 'n1a', 'n1b', 'c2', 'n2a', 'n2b', 'c3', 'n3a', 'c4', 'c5', 'n5a', 'e1', 'e2', 'e3', 'e4']
rows, seen = [], set()
for nid in order:
    for s in nodes[nid]['shots']:
        for v in ([s['then'], s.get('else')] if 'if' in s else [s]):
            if v and v.get('line') and not v.get('vo') and (v['who'], v['line']) not in seen:
                seen.add((v['who'], v['line']))
                rows.append(f"{nid}\t{v['who']}\t{v['line']}\t{v.get('sub', '')}")
open(os.path.join(HERE, '配音清单.txt'), 'w', encoding='utf-8').write(
    '# 由 build.py 生成，勿手改。段落\t角色\t原话\t普通话字幕\n' + '\n'.join(rows) + '\n')

unused = sorted(v for k, v in media_map.items() if k not in used and os.path.exists(os.path.join(OUT, v)))
print(len(used), 'media files in use;', len(rows), 'lines still need voice;', 'unused in duian/m:', ' '.join(unused) or '-')
