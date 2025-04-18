import random
import os
from typing import Dict, List, Tuple, Optional

from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class DivinationAgent:
    """
    I Ching Divination Agent — Powered by LangChain and OpenAI
    Features:
    1. Automatically generates a six-digit number (simulating traditional “hexagram casting”)
    2. Allows user to manually input a six-digit number (e.g., 385962)
    3. Converts the number into six lines (Yin/Yang) and identifies the corresponding hexagram
    4. Generates the changing hexagram based on line mutations
    5. Provides interpretations based on the user's selected inquiry type (e.g., career, love, travel, studies)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        #初始化易经占卦Agent
        """
        OpenAI API key. If set to None, it will be read from the environment variable.
        
        Args:
            api_key: Please provide an OpenAI API key or set the OPENAI_API_KEY environment variable.
        """
        api_key = api_key
        # 设置OpenAI API密钥
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        elif "OPENAI_API_KEY" not in os.environ:
            raise ValueError("Please provide an OpenAI API key or set the OPENAI_API_KEY environment variable.")
        
        # Define default model before initializing LLM
        self.model = "gpt-4o-mini"
        
        # Initialize OpenAI LLM with default model
        self.llm = OpenAI(temperature=0.7)
        
        # 初始化64卦字典
        self.hexagrams = self._init_hexagrams()
        
        # 初始化方向模板
        self.direction_templates = self._init_direction_templates()
    
    def _init_hexagrams(self) -> Dict[str, Dict]:
        """
        初始化64卦的字典
        
        Returns:
            包含64卦信息的字典
        """
        # 八卦名称
        bagua_names = {
            "111": "乾",  # 天
            "000": "坤",  # 地
            "010": "坎",  # 水
            "101": "离",  # 火
            "001": "震",  # 雷
            "110": "巽",  # 风
            "011": "艮",  # 山
            "100": "兑"   # 泽
        }
        
        # 64卦字典
        hexagrams = {}
        
        # 1. 乾为天
        hexagrams["111111"] = {
            "index": 1,
            "name": "乾为天",
            "gua_ci": "元亨利贞。",
            "xiang_yue": "天行健，君子以自强不息。"
        }
        
        # 2. 坤为地
        hexagrams["000000"] = {
            "index": 2,
            "name": "坤为地",
            "gua_ci": "元亨，利牝马之贞。君子有攸往，先迷后得主。利西南得朋，东北丧朋。安贞吉。",
            "xiang_yue": "地势坤，君子以厚德载物。"
        }
        
        # 3. 水雷屯
        hexagrams["010001"] = {
            "index": 3,
            "name": "水雷屯",
            "gua_ci": "元亨利贞，勿用有攸往，利建侯。",
            "xiang_yue": "云雷屯，君子以经纶。"
        }
        
        # 4. 山水蒙
        hexagrams["011010"] = {
            "index": 4,
            "name": "山水蒙",
            "gua_ci": "亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。",
            "xiang_yue": "山下出泉，蒙；君子以果行育德。"
        }
        
        # 5. 水天需
        hexagrams["010111"] = {
            "index": 5,
            "name": "水天需",
            "gua_ci": "有孚，光亨，贞吉。利涉大川。",
            "xiang_yue": "云上于天，需；君子以饮食宴乐。"
        }
        
        # 6. 天水讼
        hexagrams["111010"] = {
            "index": 6,
            "name": "天水讼",
            "gua_ci": "有孚窒惕，中吉，终凶。利见大人，不利涉大川。",
            "xiang_yue": "天与水违行，讼；君子以作事谋始。"
        }
        
        # 7. 地水师
        hexagrams["000010"] = {
            "index": 7,
            "name": "地水师",
            "gua_ci": "贞吉，无咎，有孚，中行，无所利，有攸往。",
            "xiang_yue": "地中有水，师；君子以容民畜众。"
        }
        
        # 8. 水地比
        hexagrams["010000"] = {
            "index": 8,
            "name": "水地比",
            "gua_ci": "吉。原筮元永贞，无咎。不宁方来，后夫凶。",
            "xiang_yue": "地上有水，比；先王以建万国，亲诸侯。"
        }
        
        # 9. 风天小畜
        hexagrams["110111"] = {
            "index": 9,
            "name": "风天小畜",
            "gua_ci": "亨。密云不雨，自我西郊。",
            "xiang_yue": "风行天上，小畜；君子以懿文德。"
        }
        
        # 10. 天泽履
        hexagrams["111100"] = {
            "index": 10,
            "name": "天泽履",
            "gua_ci": "履虎尾，不咥人，亨。",
            "xiang_yue": "上天下泽，履；君子以辨上下，定民志。"
        }
        
        # 11. 地天泰
        hexagrams["000111"] = {
            "index": 11,
            "name": "地天泰",
            "gua_ci": "小往大来，吉亨。",
            "xiang_yue": "天地交，泰；后以财成天地之道，辅相天地之宜，以左右民。"
        }
        
        # 12. 天地否
        hexagrams["111000"] = {
            "index": 12,
            "name": "天地否",
            "gua_ci": "否之匪人，不利君子贞，大往小来。",
            "xiang_yue": "天地不交，否；君子以俭德辟难，不可荣以禄。"
        }
        
        # 13. 天火同人
        hexagrams["111101"] = {
            "index": 13,
            "name": "天火同人",
            "gua_ci": "同人于野，亨。利涉大川，利君子贞。",
            "xiang_yue": "天与火，同人；君子以类族辨物。"
        }
        
        # 14. 火天大有
        hexagrams["101111"] = {
            "index": 14,
            "name": "火天大有",
            "gua_ci": "元亨。",
            "xiang_yue": "火在天上，大有；君子以遏恶扬善，顺天休命。"
        }
        
        # 15. 地山谦
        hexagrams["000011"] = {
            "index": 15,
            "name": "地山谦",
            "gua_ci": "亨，君子有终。",
            "xiang_yue": "地中有山，谦；君子以裒多益寡，称物平施。"
        }
        
        # 16. 雷地豫
        hexagrams["001000"] = {
            "index": 16,
            "name": "雷地豫",
            "gua_ci": "利建侯行师。",
            "xiang_yue": "雷出地奋，豫；先王以作乐崇德，殷荐之上帝，以配祖考。"
        }
        
        # 17. 泽雷随
        hexagrams["100001"] = {
            "index": 17,
            "name": "泽雷随",
            "gua_ci": "元亨利贞，无咎。",
            "xiang_yue": "泽中有雷，随；君子以向晦入宴息。"
        }
        
        # 18. 山风蛊
        hexagrams["011110"] = {
            "index": 18,
            "name": "山风蛊",
            "gua_ci": "元亨，利涉大川。先甲三日，后甲三日。",
            "xiang_yue": "山下有风，蛊；君子以振民育德。"
        }
        
        # 19. 地泽临
        hexagrams["000100"] = {
            "index": 19,
            "name": "地泽临",
            "gua_ci": "元亨利贞，至于八月有凶。",
            "xiang_yue": "泽上有地，临；君子以教思无穷，容保民无疆。"
        }
        
        # 20. 风地观
        hexagrams["110000"] = {
            "index": 20,
            "name": "风地观",
            "gua_ci": "盥而不荐，有孚颙若。",
            "xiang_yue": "风行地上，观；先王以省方观民设教。"
        }
        
        # 21. 火雷噬嗑
        hexagrams["101001"] = {
            "index": 21,
            "name": "火雷噬嗑",
            "gua_ci": "亨。利用狱。",
            "xiang_yue": "雷电噬嗑；君子以慎罚足以警。"
        }
        
        # 22. 山火贲
        hexagrams["011101"] = {
            "index": 22,
            "name": "山火贲",
            "gua_ci": "亨。小利有攸往。",
            "xiang_yue": "山下有火，贲；君子以明庶政，无敢折狱。"
        }
        
        # 23. 山地剥
        hexagrams["011000"] = {
            "index": 23,
            "name": "山地剥",
            "gua_ci": "不利有攸往。",
            "xiang_yue": "山附于地，剥；上以厚下，安宅。"
        }
        
        # 24. 地雷复
        hexagrams["000001"] = {
            "index": 24,
            "name": "地雷复",
            "gua_ci": "亨。出入无疾，朋来无咎。反复其道，七日来复，利有攸往。",
            "xiang_yue": "雷在地中，复；先王以至日闭关，商旅不行，后不省方。"
        }
        
        # 25. 天雷无妄
        hexagrams["111001"] = {
            "index": 25,
            "name": "天雷无妄",
            "gua_ci": "元亨利贞。其匪正有眚，不利有攸往。",
            "xiang_yue": "天下雷行，物与无妄；先王以茂对时，育万物。"
        }
        
        # 26. 山天大畜
        hexagrams["011111"] = {
            "index": 26,
            "name": "山天大畜",
            "gua_ci": "利贞，不家食吉，利涉大川。",
            "xiang_yue": "天在山中，大畜；君子以多识前言往行，以畜其德。"
        }
        
        # 27. 山雷颐
        hexagrams["011001"] = {
            "index": 27,
            "name": "山雷颐",
            "gua_ci": "贞吉。观颐，自求口实。",
            "xiang_yue": "山下有雷，颐；君子以慎言语，节饮食。"
        }
        
        # 28. 泽风大过
        hexagrams["100110"] = {
            "index": 28,
            "name": "泽风大过",
            "gua_ci": "栋挠，利有攸往，亨。",
            "xiang_yue": "泽灭木，大过；君子以独立不惧，遁世无闷。"
        }
        
        # 29. 坎为水
        hexagrams["010010"] = {
            "index": 29,
            "name": "坎为水",
            "gua_ci": "习坎，有孚，维心亨，行有尚。",
            "xiang_yue": "水洊至，习坎；君子以常德行，习教事。"
        }
        
        # 30. 离为火
        hexagrams["101101"] = {
            "index": 30,
            "name": "离为火",
            "gua_ci": "利贞，亨。畜牝牛，吉。",
            "xiang_yue": "明两作，离；大人以继明照于四方。"
        }
        
        # 31. 泽山咸
        hexagrams["100011"] = {
            "index": 31,
            "name": "泽山咸",
            "gua_ci": "亨，利贞，取女吉。",
            "xiang_yue": "山上有泽，咸；君子以虚受人。"
        }
        
        # 32. 雷风恒
        hexagrams["001110"] = {
            "index": 32,
            "name": "雷风恒",
            "gua_ci": "亨，无咎，利贞，利有攸往。",
            "xiang_yue": "雷风，恒；君子以立不易方。"
        }
        
        # 33. 天山遁
        hexagrams["111011"] = {
            "index": 33,
            "name": "天山遁",
            "gua_ci": "亨，小利贞。",
            "xiang_yue": "天下有山，遁；君子以远小人，不恶而严。"
        }
        
        # 34. 雷天大壮
        hexagrams["001111"] = {
            "index": 34,
            "name": "雷天大壮",
            "gua_ci": "利贞。",
            "xiang_yue": "雷在天上，大壮；君子以非礼弗履。"
        }
        
        # 35. 火地晋
        hexagrams["101000"] = {
            "index": 35,
            "name": "火地晋",
            "gua_ci": "晋如，康侯用锡马蕃庶，昼日三接。",
            "xiang_yue": "明出地上，晋；君子以自昭明德。"
        }
        
        # 36. 地火明夷
        hexagrams["000101"] = {
            "index": 36,
            "name": "地火明夷",
            "gua_ci": "利艰贞。",
            "xiang_yue": "明入地中，明夷；君子以莅众，用晦而明。"
        }
        
        # 37. 风火家人
        hexagrams["110101"] = {
            "index": 37,
            "name": "风火家人",
            "gua_ci": "利女贞。",
            "xiang_yue": "风自火出，家人；君子以言有物而行有恒。"
        }
        
        # 38. 火泽睽
        hexagrams["101100"] = {
            "index": 38,
            "name": "火泽睽",
            "gua_ci": "小事吉。",
            "xiang_yue": "上火下泽，睽；君子以同而异。"
        }
        
        # 39. 水山蹇
        hexagrams["010011"] = {
            "index": 39,
            "name": "水山蹇",
            "gua_ci": "利西南，不利东北；利见大人，贞吉。",
            "xiang_yue": "山上有水，蹇；君子以反身修德。"
        }
        
        # 40. 雷水解
        hexagrams["001010"] = {
            "index": 40,
            "name": "雷水解",
            "gua_ci": "利西南，无所往，其来复吉。有攸往，夙吉。",
            "xiang_yue": "雷雨作，解；君子以赦过宥罪。"
        }
        
        # 41. 山泽损
        hexagrams["011100"] = {
            "index": 41,
            "name": "山泽损",
            "gua_ci": "有孚，元吉，无咎，可贞，利有攸往。曷之用，二簋可用享。",
            "xiang_yue": "山下有泽，损；君子以惩忿窒欲。"
        }
        
        # 42. 风雷益
        hexagrams["110001"] = {
            "index": 42,
            "name": "风雷益",
            "gua_ci": "利有攸往，利涉大川。",
            "xiang_yue": "风雷，益；君子以见善则迁，有过则改。"
        }
        
        # 43. 泽天夬
        hexagrams["100111"] = {
            "index": 43,
            "name": "泽天夬",
            "gua_ci": "扬于王庭，孚号，有厉，告自邑，不利即戎，利有攸往。",
            "xiang_yue": "泽上于天，夬；君子以施禄及下，居德则忌。"
        }
        
        # 44. 天风姤
        hexagrams["111110"] = {
            "index": 44,
            "name": "天风姤",
            "gua_ci": "女壮，勿用取女。",
            "xiang_yue": "天下有风，姤；后以施命诰四方。"
        }
        
        # 45. 泽地萃
        hexagrams["100000"] = {
            "index": 45,
            "name": "泽地萃",
            "gua_ci": "亨。王假有庙，利见大人，亨，利贞。用大牲吉，利有攸往。",
            "xiang_yue": "泽上于地，萃；君子以除戎器，戒不虞。"
        }
        
        # 46. 地风升
        hexagrams["000110"] = {
            "index": 46,
            "name": "地风升",
            "gua_ci": "元亨，用见大人，勿恤，南征吉。",
            "xiang_yue": "地中生木，升；君子以顺德，积小以高大。"
        }
        
        # 47. 泽水困
        hexagrams["100010"] = {
            "index": 47,
            "name": "泽水困",
            "gua_ci": "亨，贞，大人吉，无咎，有言不信。",
            "xiang_yue": "泽无水，困；君子以致命遂志。"
        }
        
        # 48. 水风井
        hexagrams["010110"] = {
            "index": 48,
            "name": "水风井",
            "gua_ci": "改邑不改井，无丧无得，往来井井。汔至，亦未繘井，羸其瓶，凶。",
            "xiang_yue": "木上有水，井；君子以劳民劝相。"
        }
        
        # 49. 泽火革
        hexagrams["100101"] = {
            "index": 49,
            "name": "泽火革",
            "gua_ci": "巳日乃孚，元亨利贞，悔亡。",
            "xiang_yue": "泽中有火，革；君子以治历明时。"
        }
        
        # 50. 火风鼎
        hexagrams["101110"] = {
            "index": 50,
            "name": "火风鼎",
            "gua_ci": "元吉，亨。",
            "xiang_yue": "木上有火，鼎；君子以正位凝命。"
        }
        
        # 51. 震为雷
        hexagrams["001001"] = {
            "index": 51,
            "name": "震为雷",
            "gua_ci": "亨。震来虩虩，笑言哑哑。震惊百里，不丧匕鬯。",
            "xiang_yue": "洊雷，震；君子以恐惧修省。"
        }
        
        # 52. 艮为山
        hexagrams["011011"] = {
            "index": 52,
            "name": "艮为山",
            "gua_ci": "艮其背，不获其身，行其庭，不见其人，无咎。",
            "xiang_yue": "兼山，艮；君子以思不出其位。"
        }
        
        # 53. 风山渐
        hexagrams["110011"] = {
            "index": 53,
            "name": "风山渐",
            "gua_ci": "女归吉，利贞。",
            "xiang_yue": "山上有木，渐；君子以居贤德善俗。"
        }
        
        # 54. 雷泽归妹
        hexagrams["001100"] = {
            "index": 54,
            "name": "雷泽归妹",
            "gua_ci": "征凶，无攸利。",
            "xiang_yue": "泽上有雷，归妹；君子以永终知敝。"
        }
        
        # 55. 雷火丰
        hexagrams["001101"] = {
            "index": 55,
            "name": "雷火丰",
            "gua_ci": "亨，王假之，勿忧，宜日中。",
            "xiang_yue": "雷电皆至，丰；君子以折狱致刑。"
        }
        
        # 56. 火山旅
        hexagrams["101011"] = {
            "index": 56,
            "name": "火山旅",
            "gua_ci": "小亨，旅贞吉。",
            "xiang_yue": "山上有火，旅；君子以明慎用刑，而不留狱。"
        }
        
        # 57. 巽为风
        hexagrams["110110"] = {
            "index": 57,
            "name": "巽为风",
            "gua_ci": "小亨，利有攸往，利见大人。",
            "xiang_yue": "随风，巽；君子以申命行事。"
        }
        
        # 58. 兑为泽
        hexagrams["100100"] = {
            "index": 58,
            "name": "兑为泽",
            "gua_ci": "亨，利贞。",
            "xiang_yue": "丽泽，兑；君子以朋友讲习。"
        }
        
        # 59. 风水涣
        hexagrams["110010"] = {
            "index": 59,
            "name": "风水涣",
            "gua_ci": "亨，王假有庙，利涉大川，利贞。",
            "xiang_yue": "风行水上，涣；先王以享于帝，立庙。"
        }
        
        # 60. 水泽节
        hexagrams["010100"] = {
            "index": 60,
            "name": "水泽节",
            "gua_ci": "亨，苦节不可贞。",
            "xiang_yue": "泽上有水，节；君子以制数度，议德行。"
        }
        
        # 61. 风泽中孚
        hexagrams["110100"] = {
            "index": 61,
            "name": "风泽中孚",
            "gua_ci": "豚鱼吉，利涉大川，利贞。",
            "xiang_yue": "泽上有风，中孚；君子以议狱缓死。"
        }
        
        # 62. 雷山小过
        hexagrams["001011"] = {
            "index": 62,
            "name": "雷山小过",
            "gua_ci": "亨，利贞，可小事，不可大事。飞鸟遗之音，不宜上，宜下，大吉。",
            "xiang_yue": "山上有雷，小过；君子以行过乎恭，丧过乎哀，用过乎俭。"
        }
        
        # 63. 水火既济
        hexagrams["010101"] = {
            "index": 63,
            "name": "水火既济",
            "gua_ci": "亨，小利贞，初吉终乱。",
            "xiang_yue": "水在火上，既济；君子以思患而豫防之。"
        }
        
        # 64. 火水未济
        hexagrams["101010"] = {
            "index": 64,
            "name": "火水未济",
            "gua_ci": "亨，小狐汔济，濡其尾，无攸利。",
            "xiang_yue": "火在水上，未济；君子以慎辨物居方。"
        }
        
        return hexagrams
    
    def _init_direction_templates(self) -> Dict[str, Dict]:
        """
        Initialize inquiry direction templates.
        
        Returns:
            A dictionary containing templates for different inquiry directions.
        """
        templates = {
                "Travel": {
                    "keywords": [
                    "travel", "trip", "journey", "vacation", "holiday", "outing", "go out", "leave home",
                    "go abroad", "road trip", "flight", "airport", "train", "travel plan", "traveling",
                    "travelled", "traveling soon", "where should I go", "travel schedule", "tour",
                    "backpacking", "travel luck", "travel forecast", "safe trip", "trip blessing",
                    "adventure", "moving around", "commute", "commuting", "travel vibes", 
                    "weather for travel", "is it good to travel", "start a journey", "travel energy",
                    "suitcase", "passport", "ride", "relocation", "business trip", "travel direction",
                    "leave for", "is it a good time to travel", "vacation plans", "leaving town",
                    "I’m traveling", "trip ahead", "transit", "transit luck", "travel delay", "trip today",
                    "出行", "出行运", "旅行", "旅游", "远行", "出门", "动身", "外出", "走亲戚", "出差", "通勤", 
                    "探亲", "行程", "行走", "动向", "出游", "旅程", "在路上", "乘车", "火车", "飞机", "登机",
                    "签证", "护照", "行李", "搬家", "离开", "探访", "是否适合出行", "适合出门吗"
                ],
                "prompt_template": """Analyze travel fortune based on the I Ching hexagram:
        Original Hexagram: {original_hexagram_name} (Index {original_hexagram_index})
        Changing Hexagram: {changed_hexagram_name} (Index {changed_hexagram_index})

        Hexagram Text: "{original_gua_ci}"
        Image Text: "{original_xiang_yue}"

        Based on the above information, please analyze the user's current travel fortune, and provide specific advice along with a poetic signature for the day.
        Advice may include: whether it's a good time to travel, ideal time periods, and any cautions to keep in mind.
        The signature quote should be a proverb or poetic line that aligns with the hexagram's meaning.
        """
                },
                    "Love": {
                        "keywords": [
                        "love", "relationship", "romance", "marriage", "partner", "couple", "dating", "breakup",
                        "falling in love", "get back together", "heartbreak", "affection", "wedding", "emotion",
                        "情感", "感情", "恋爱", "爱情", "爱人", "约会", "关系", "婚姻", "姻缘", "脱单", "分手",
                        "复合", "暧昧", "表白", "示爱", "对象", "结婚", "心动", "配对", "感情建议", "恋情"
                    ],
                    "prompt_template": """Analyze love fortune based on the I Ching hexagram:
        Original Hexagram: {original_hexagram_name} (Index {original_hexagram_index})
        Changing Hexagram: {changed_hexagram_name} (Index {changed_hexagram_index})

        Hexagram Text: "{original_gua_ci}"
        Image Text: "{original_xiang_yue}"

        Based on the above information, please analyze the user's current romantic fortune, and provide practical guidance and a poetic signature.
        Advice may include: relationship dynamics, emotional tendencies, communication strategies, and other notes.
        The signature quote should be a proverb or poetic line that reflects the meaning of the hexagram.
        """
                },
                        "Career": {
                            "keywords": [
                        "career", "job", "work", "promotion", "entrepreneurship", "boss", "colleague", "office",
                        "interview", "fired", "resign", "salary", "quit job", "change job", "new job",
                        "employment", "job offer", "workplace", "company", "job hunt", "hiring", "get hired",
                        "职场", "工作", "职业", "事业", "升职", "加薪", "老板", "同事", "面试", "离职", "跳槽",
                        "创业", "换工作", "裁员", "找工作", "上班", "就业", "公司", "职业发展", "工作运势"
                    ],
                    "prompt_template": """Analyze career fortune based on the I Ching hexagram:
        Original Hexagram: {original_hexagram_name} (Index {original_hexagram_index})
        Changing Hexagram: {changed_hexagram_name} (Index {changed_hexagram_index})

        Hexagram Text: "{original_gua_ci}"
        Image Text: "{original_xiang_yue}"

        Based on the above information, please analyze the user's current career outlook, and provide actionable insights and a poetic signature.
        Advice may include: development trends, decision-making strategies, opportunities to watch for, and risks to avoid.
        The signature quote should be a proverb or poetic line that corresponds with the hexagram’s symbolism.
        """
                },
                    "Study": {
                        "keywords": [
                        "study", "exam", "learning", "education", "research", "school", "test", "grade", 
                        "student", "academic", "homework", "midterm", "final", "study luck", "academic outlook",
                        "pass the exam", "good score", "考试", "学业", "成绩", "学习", "升学", "研究", "功课", "考运",
                        "备考", "学生", "应试", "分数", "学期", "读书", "书本", "课业", "学习运势", "学术发展"
                    ],
                    "prompt_template": """Analyze academic fortune based on the I Ching hexagram:
        Original Hexagram: {original_hexagram_name} (Index {original_hexagram_index})
        Changing Hexagram: {changed_hexagram_name} (Index {changed_hexagram_index})

        Hexagram Text: "{original_gua_ci}"
        Image Text: "{original_xiang_yue}"

        Based on the above information, please analyze the user's academic fortune, and provide personalized advice and a poetic signature.
        Advice may include: learning efficiency, exam outlook, mental focus, and recommended adjustments.
        The signature quote should be a proverb or poetic line aligned with the message of the hexagram.
        """
                        }
                }

        return templates
    
    def generate_random_numbers(self) -> str:
        """
        Generate a six-digit random number (simulate hexagram casting)
        
        Returns:
            A string of six random digits.
        """
        return ''.join([str(random.randint(1, 9)) for _ in range(6)])
    
    def numbers_to_yao(self, numbers: str) -> List[int]:
        """
        Convert a 6-digit number string into a list of six Yao lines.
        
        Args:
            numbers: A string of exactly 6 digits.
            
        Returns:
            A list of six integers, where 0 represents a Yin line and 1 represents a Yang line.
        """
        if not numbers or len(numbers) != 6 or not numbers.isdigit():
            raise ValueError("Please provide a valid 6-digit number.")
        
        # 将每个数字对2取余，奇数为阳爻（1），偶数为阴爻（0）
        return [int(int(num) % 2) for num in numbers]
    
    def yao_to_hexagram(self, yao: List[int]) -> str:
        """
        Convert a list of six Yao (Yin/Yang) lines into a hexagram binary code.
        
        Args:
            yao: A list of six integers, where 0 represents a Yin line and 1 represents a Yang line.
            
        Returns:
            A string representing the binary code of the hexagram（e.g.,"010010"for坎为水）
        """
        return ''.join([str(y) for y in yao])
    
    def generate_changed_hexagram(self, yao: List[int], numbers: str) -> str:
        """
        Generate the changing hexagram based on the original yao lines and the corresponding digit string.
        
        Args:
            yao: A list of six integers representing the original hexagram lines (0 = Yin, 1 = Yang)
            numbers: A 6-digit string used to determine which lines are changing
            
        Returns:
            The binary code of the resulting changing hexagram (e.g., "110100")
        """
        # 根据数字的大小决定是否变爻（数字为6或9时变爻）
        changed_yao = yao.copy()
        for i, num in enumerate(numbers):
            if num in ['6', '9']:  # 6和9为变爻数字
                changed_yao[i] = 1 - changed_yao[i]  # 阴变阳，阳变阴
        
        return self.yao_to_hexagram(changed_yao)
    
    def get_direction(self, query: str) -> str:
        """
        Determine the inquiry direction based on user input.
        
        Args:
            query: The user's input question or statement.
            
        Returns:
            The matched inquiry direction (e.g., 'Travel', 'Love', 'Career', or 'Study').
        """
        # 默认方向
        default_direction = "Travel"
        
        # 遍历方向模板，查找匹配的关键词
        for direction, info in self.direction_templates.items():
            for keyword in info["keywords"]:
                if keyword in query:
                    return direction
        
        # 如果没有匹配到关键词，返回默认方向
        return default_direction
    
    def generate_interpretation(self, original_hexagram: Dict, changed_hexagram: Dict, direction: str) -> str:
        """
        Generate an interpretation of the hexagram based on the original and changing hexagrams,
        as well as the user's inquiry direction.
        
        Args:
            original_hexagram: A dictionary containing details of the original hexagram.
            changed_hexagram: A dictionary containing details of the changing hexagram.
            direction: The user's inquiry type (e.g., 'Travel', 'Love', 'Career', 'Study').
            
        Returns:
            A formatted interpretation string generated by the language model.
        """
        # 获取方向对应的提示模板
        prompt_template = self.direction_templates[direction]["prompt_template"]
        
        # 填充模板
        prompt = prompt_template.format(
            original_hexagram_name=original_hexagram["name"],
            original_hexagram_index=original_hexagram["index"],
            changed_hexagram_name=changed_hexagram["name"],
            changed_hexagram_index=changed_hexagram["index"],
            original_gua_ci=original_hexagram["gua_ci"],
            original_xiang_yue=original_hexagram["xiang_yue"]
        )
        
        # 使用LangChain生成解释
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(prompt)
        )
        
        interpretation = chain.run({})
        
        # 格式化输出
        result = f"""🔢 Original Hexagram: {original_hexagram['name']} (Index {original_hexagram['index']})
🔁 Changing Hexagram: {changed_hexagram['name']} (Index {changed_hexagram['index']})

📖 Hexagram Text: "{original_hexagram['gua_ci']}"
🗣 Image Commentary: "{original_hexagram['xiang_yue']}"

🎯 Your inquiry type: "{direction}"
{interpretation}"""
        
        return result
    
    def divine(self, numbers: Optional[str] = None, query: str = "Travel") -> str:
        """
        Perform a divination process.
        
        Args:
            numbers: A 6-digit string. If None, a random number will be generated automatically.
            query: The user's question or inquiry (e.g., "Love", "Career", "Travel").
            
        Returns:
            The final divination result string.
        """
        # 如果没有提供数字，则自动生成
        if numbers is None:
            numbers = self.generate_random_numbers()
            print(f"Auto-generated number：{numbers}")
        
        # 将数字转换为六爻
        yao = self.numbers_to_yao(numbers)
        
        # 将六爻转换为卦象编码
        hexagram_code = self.yao_to_hexagram(yao)
        
        # 获取本卦信息
        if hexagram_code not in self.hexagrams:
            raise ValueError(f"Unable to find matching hexagram：{hexagram_code}")
        original_hexagram = self.hexagrams[hexagram_code]
        
        # 生成变卦
        changed_hexagram_code = self.generate_changed_hexagram(yao, numbers)
        
        # 获取变卦信息
        if changed_hexagram_code not in self.hexagrams:
            raise ValueError(f"Unable to find matching changing hexagram：{changed_hexagram_code}")
        changed_hexagram = self.hexagrams[changed_hexagram_code]
        
        # 确定问事方向
        direction = self.get_direction(query)
        
        # 生成解释
        result = self.generate_interpretation(original_hexagram, changed_hexagram, direction)
        
        return result
