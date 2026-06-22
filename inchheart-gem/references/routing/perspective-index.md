# Perspective Index

这是 `inchheart-gem` 的人物视角索引。当前共 86 个 perspective（视角）。

## 使用规则

- 默认从 `inchheart-gem` 主入口路由。
- 只有用户点名人物/主题，或需求明显匹配某个思维框架时，才读取对应卡片。
- 普通人物读取路径：`references/perspectives/<id>/PERSPECTIVE.md`。
- 酒馆人物读取路径：`references/tavern/<id>/PERSPECTIVE.md`。
- 点名人物时，读取该人物目录下 `references/**/*.md` 的全部 Markdown 研究材料；不读取脚本、缓存、图片或非 Markdown 文件。
- 触发“闲聊酒馆”时，先读 `tavern-routing.md/json`，只从酒馆成员中随机 1 位主聊人物。
- 人物视角优先沉浸：允许第一人称、锋利判断和人物偏见；只在现实事实、专业处置或身份混淆时简短澄清来源。

### AI 与科技创业（12 位）

| 中文/英文名 | Perspective | 路径 | 何时调用 |
|---|---|---|---|
| Andrej Karpathy | `andrej-karpathy-perspective` | `references/perspectives/andrej-karpathy-perspective/PERSPECTIVE.md` | Andrej Karpathy的思维框架与表达方式。基于20+篇博文、16段深度访谈、100+条X帖子的系统蒸馏， 提炼6个核心心智模型、8条决策启发式、完整的中文输出适配和经典句式速查。 用途：作为思维顾问，用Karpathy的视角分析AI技术可靠性、学习方法、行业趋势、产品设计。 当用户提到「用Karpathy的… |
| Dario Amodei | `dario-amodei-perspective` | `references/perspectives/dario-amodei-perspective/PERSPECTIVE.md` | Dario Amodei的思维框架与表达方式。基于Dario本人长文、Anthropic官方安全研究、Scaling Laws论文、 Constitutional AI、Responsible Scaling Policy、可解释性研究和公开访谈材料的初版调研， 提炼6个核心心智模型、8条决策启发式和完整的中文表达D… |
| Ilya Sutskever | `ilya-sutskever-perspective` | `references/perspectives/ilya-sutskever-perspective/PERSPECTIVE.md` | Ilya Sutskever的思维框架与表达方式。基于12段一手对话、9篇学术论文、10小时宣誓证词、 27篇推荐阅读清单和14个权威二手来源的深度调研， 提炼6个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用Ilya的视角分析AI技术方向、安全策略、研究品味。 当用户提到「用Ilya的视角… |
| Ken Thompson | `ken-thompson-perspective` | `references/perspectives/ken-thompson-perspective/PERSPECTIVE.md` | Kenneth Lane Thompson 的思维框架与表达方式。基于 Unix、B 语言、C 语言源流、Plan 9、Go、 UTF-8、信任编译器攻击、访谈与同事回忆的系统蒸馏，提炼 6 个核心心智模型、8 条决策启发式、 工程审美与中文输出适配。 用途：作为思维顾问，用 Ken Thompson 的视角分析操作… |
| Sam Altman | `sam-altman-perspective` | `references/perspectives/sam-altman-perspective/PERSPECTIVE.md` | Sam Altman的思维框架与表达方式。基于博客、访谈、YC经历、OpenAI公开资料、投资和外部评论的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用Sam Altman的视角分析创业、AI、资本配置、平台、速度、招聘、AGI叙事和组织决策。 当用户提到「Sam Altman… |
| Paul Graham | `paul-graham-perspective` | `references/perspectives/paul-graham-perspective/PERSPECTIVE.md` | Paul Graham的思维框架与表达方式。基于200+篇essays、12个播客/访谈、 Twitter/X分析、7位核心批评者视角和完整人生时间线的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用PG的视角分析创业、写作、产品和人生选择。 当用户提到「用PG的视角」「P… |
| 张一鸣 | `zhang-yiming-perspective` | `references/perspectives/zhang-yiming-perspective/PERSPECTIVE.md` | 张一鸣（字节跳动/TikTok创始人）的思维框架与表达方式。基于6个维度（著作、深度访谈、 表达DNA、他者视角、决策记录、时间线）的调研，涵盖32个访谈片段、12个重大决策案例， 提炼5个核心心智模型、7条决策启发式和完整的表达DNA。 用途：作为思维顾问，用张一鸣的视角分析产品、组织、全球化、人才和个人成长问题。… |
| 张小龙 | `zhang-xiaolong-perspective` | `references/perspectives/zhang-xiaolong-perspective/PERSPECTIVE.md` | 张小龙的产品思维框架与表达方式。基于腾讯公司资料、微信公开课长演讲、腾讯大讲堂产品分享、 公开报道和长文本访谈材料提炼。 用途：作为产品与平台视角顾问，用张小龙式方法分析社交产品、工具产品、平台生态、功能克制、用户体验和产品价值观。 当用户提到「张小龙视角」「微信产品观」「小而美」「产品经理视角」「克制的产品设计」「… |
| Jeff Bezos | `jeff-bezos-perspective` | `references/perspectives/jeff-bezos-perspective/PERSPECTIVE.md` | Jeff Bezos 的思维框架与表达方式。基于 Amazon 股东信、公开访谈、演讲和公司决策材料， 提炼 5 个核心心智模型、8 条决策启发式和表达 DNA。 用途：作为思维顾问，用 Bezos 视角分析客户价值、长期主义、发明、组织机制、资本配置和高速度决策。 当用户提到「Bezos 视角」「Jeff Bezo… |
| 马斯克 | `elon-musk-perspective` | `references/perspectives/elon-musk-perspective/PERSPECTIVE.md` | 马斯克的思维操作系统。基于传记、播客、推文、法庭证词、决策记录和外部批评的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用马斯克的视角分析问题、审视决策、拆解成本结构、挑战行业假设。 当用户提到「用马斯克的视角」「马斯克会怎么看」「Musk模式」「马斯克perspectiv… |
| 史蒂夫·乔布斯 | `steve-jobs-perspective` | `references/perspectives/steve-jobs-perspective/PERSPECTIVE.md` | 史蒂夫·乔布斯(Steve Jobs)的思维框架与表达方式。基于Isaacson授权传记、Stanford演讲、 Lost Interview、D Conference系列、Make Something Wonderful、30+一手来源的深度调研， 提炼6个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作… |
| 杰弗里·辛顿 | `geoffrey-hinton-perspective` | `references/perspectives/geoffrey-hinton-perspective/PERSPECTIVE.md` | 杰弗里·辛顿的科学思维框架与表达方式。基于大学、诺奖、ACM、论文与访谈资料， 提炼4个核心心智模型、7条决策启发式和完整表达DNA。 用途：作为思维顾问，用辛顿视角分析神经网络、AI风险、研究判断、教育与技术路线选择。 当用户提到「辛顿视角」「Hinton perspective」「深度学习」「AI风险」「神经网络… |

### 商业、投资与增长（7 位）

| 中文/英文名 | Perspective | 路径 | 何时调用 |
|---|---|---|---|
| 段永平 | `duan-yongping-perspective` | `references/perspectives/duan-yongping-perspective/PERSPECTIVE.md` | 段永平的商业、组织和投资思维框架。基于公开长访谈、雪球公开对话、公司资料、权威媒体报道、 OPPO/vivo公开资料和投资相关公开文件提炼。 用途：作为商业与投资视角顾问，用段永平式方法分析本分、消费者导向、好公司、长期主义、分权管理和能力圈。 当用户提到「段永平视角」「本分」「消费者导向」「买股票就是买公司」「步步… |
| 查理·芒格 | `munger-perspective` | `references/perspectives/munger-perspective/PERSPECTIVE.md` | 查理·芒格的思维框架与表达方式。基于《穷查理宝典》、伯克希尔/Daily Journal股东会、 USC/哈佛演讲、访谈记录、外部批评等50+来源的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用芒格的视角分析问题、审视决策、提供反馈。 当用户提到「用芒格的视角」「芒格会怎… |
| 沃伦·巴菲特 | `warren-buffett-perspective` | `references/perspectives/warren-buffett-perspective/PERSPECTIVE.md` | 沃伦·巴菲特的思维框架与表达方式。基于股东信、伯克希尔年会、访谈、投资案例和外部研究的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用巴菲特的视角分析长期投资、商业质量、能力圈、护城河、资本配置和风险。 当用户提到「巴菲特视角」「巴菲特会怎么看」「价值投资」「护城河」「能力圈」「… |
| Naval Ravikant | `naval-perspective` | `references/perspectives/naval-perspective/PERSPECTIVE.md` | Naval Ravikant的思维操作系统。基于著作、播客、推文、决策记录和外部批评的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 激活后沉浸式扮演Naval，直接以「我」的视角回应问题。 当用户提到「用Naval的视角」「Naval会怎么看」「纳瓦尔模式」「Naval perspective… |
| 塔勒布 | `taleb-perspective` | `references/perspectives/taleb-perspective/PERSPECTIVE.md` | 塔勒布(Nassim Nicholas Taleb)的思维框架与表达方式。基于40+个来源的深度调研， 提炼6个核心心智模型、9条决策启发式和完整的表达DNA。 用途：作为思维顾问，用塔勒布的视角分析问题、审视决策、质疑主流叙事。 当用户提到「用塔勒布的视角」「塔勒布会怎么看」「塔勒布模式」「反脆弱视角」「taleb… |
| 亚当·斯密 | `adamsmith-perspective` | `references/perspectives/adamsmith-perspective/PERSPECTIVE.md` | 亚当·斯密的公开思维框架。外部领域：国富论/看不见的手/分工。从 Panmax/awesome-nuwa 的 Panmax/adamsmith-skill 转换导入。 |
| 哈耶克 | `hayek-perspective` | `references/perspectives/hayek-perspective/PERSPECTIVE.md` | 哈耶克的公开思维框架。外部领域：自由市场/自发秩序/知识论。从 Panmax/awesome-nuwa 的 Panmax/hayek-skill 转换导入。 |

### 哲学、理论与宗教（23 位）

| 中文/英文名 | Perspective | 路径 | 何时调用 |
|---|---|---|---|
| 汉娜·阿伦特 | `hannah-arendt-perspective` | `references/perspectives/hannah-arendt-perspective/PERSPECTIVE.md` | 汉娜·阿伦特的思维框架与表达方式。基于《极权主义的起源》《人的境况》《艾希曼在耶路撒冷》、 《过去与未来之间》、访谈和权威研究资料，提炼 5 个核心心智模型、8 条判断启发式和表达 DNA。 用途：作为思维顾问，用阿伦特视角分析行动、公共领域、极权主义、责任、判断、恶与思想贫乏。 当用户提到「阿伦特视角」「Hanna… |
| 罗兰·巴特 | `roland-barthes-perspective` | `references/perspectives/roland-barthes-perspective/PERSPECTIVE.md` | 罗兰·巴特的思维框架与表达方式。基于《神话学》《符号学原理》《S/Z》《作者之死》《罗兰·巴特论罗兰·巴特》《明室》、 出版社资料、百科资料和权威批评资料的初版调研，提炼5个核心心智模型、8条启发式和表达DNA。 用途：作为思维顾问，用巴特视角分析符号、神话、流行文化、文本、摄影、作者、读者、欲望和日常意识形态。 当… |
| 苏珊·桑塔格 | `susan-sontag-perspective` | `references/perspectives/susan-sontag-perspective/PERSPECTIVE.md` | 苏珊·桑塔格的思维框架与表达方式。基于《反对阐释》《论摄影》《疾病的隐喻》《艾滋病及其隐喻》《旁观他人之痛》、 访谈、基金会页面、出版社资料和权威文学资料的初版调研，提炼5个核心心智模型、8条启发式和表达DNA。 用途：作为思维顾问，用桑塔格视角分析艺术、摄影、疾病话语、战争图像、公共良知、审美经验和批评伦理。 当用… |
| 马歇尔·麦克卢汉 | `marshall-mcluhan-perspective` | `references/perspectives/marshall-mcluhan-perspective/PERSPECTIVE.md` | 马歇尔·麦克卢汉的思维框架与表达方式。基于《古腾堡星系》《理解媒介》《媒介即按摩》、 电视/广播访谈、McLuhan Speaks 档案和权威研究资料提炼。 用途：作为思维顾问，用麦克卢汉视角分析媒介、技术、感官、教育、广告、平台、AI 与社会变形。 当用户提到「麦克卢汉视角」「媒介即讯息」「地球村」「热媒介/冷媒介… |
| 卡尔·荣格 | `carl-jung-perspective` | `references/perspectives/carl-jung-perspective/PERSPECTIVE.md` | 卡尔·荣格的思维框架与表达方式。基于著作、访谈、病例思想、回忆录材料和心理学史研究的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用荣格的视角分析梦、阴影、人格整合、原型、个体化和象征问题。 当用户提到「荣格视角」「荣格会怎么看」「阴影」「原型」「个体化」「梦分析」「集体无意识」… |
| 德勒兹 | `deleuze-perspective` | `references/perspectives/deleuze-perspective/PERSPECTIVE.md` | 德勒兹的思维框架与表达方式。基于著作、访谈/节目、公开资料和权威二手资料的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用德勒兹的视角分析艺术、哲学、文化和个人判断问题。 当用户提到「德勒兹视角」「德勒兹会怎么看」「德勒兹视角、根茎、生成、差异、褶子、欲望机器、游牧、电影哲学」时… |
| 福柯 | `foucault-perspective` | `references/perspectives/foucault-perspective/PERSPECTIVE.md` | 福柯的思维框架与表达方式。基于著作、访谈/节目、公开资料和权威二手资料的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用福柯的视角分析艺术、哲学、文化和个人判断问题。 当用户提到「福柯视角」「福柯会怎么看」「福柯视角、权力知识、规训、谱系学、考古学、生命政治、监狱、疯癫、主体化」… |
| 尼采 | `nietzsche-perspective` | `references/perspectives/nietzsche-perspective/PERSPECTIVE.md` | 尼采的思维框架与表达方式。基于著作、访谈/节目、公开资料和权威二手资料的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用尼采的视角分析艺术、哲学、文化和个人判断问题。 当用户提到「尼采视角」「尼采会怎么看」「尼采视角、价值重估、谱系学、超人、虚无主义、酒神、透视主义、权力意志」时… |
| 齐泽克 | `zizek-perspective` | `references/perspectives/zizek-perspective/PERSPECTIVE.md` | 齐泽克的思维框架与表达方式。基于著作、访谈/文本、权威传记和外部评价的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用齐泽克的视角分析意识形态、犬儒主义、拉康/黑格尔、流行文化、政治幻象和主体困境。 当用户提到「齐泽克视角」「齐泽克会怎么看」「齐泽克视角、意识形态、拉康、黑格尔、… |
| 卡尔·马克思 | `karl-marx-perspective` | `references/perspectives/karl-marx-perspective/PERSPECTIVE.md` | 卡尔·马克思的思维框架与表达方式。基于著作、书信、政治经济学批判、历史研究和外部解释的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用马克思的视角分析资本、阶级、劳动、意识形态、商品、历史结构和现代社会矛盾。 当用户提到「马克思视角」「马克思会怎么看」「资本论」「阶级」「商品拜物… |
| 拿撒勒人耶稣 | `jesus-of-nazareth-perspective` | `references/perspectives/jesus-of-nazareth-perspective/PERSPECTIVE.md` | 拿撒勒人耶稣的思维框架与表达方式。基于福音书文本、历史耶稣研究、早期基督教背景和外部研究的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用耶稣的视角分析怜悯、悔改、权力、财富、宽恕、比喻和边缘者处境。 当用户提到「耶稣视角」「耶稣会怎么看」「福音书」「登山宝训」「比喻」「宽恕」「… |
| 第十四世达赖喇嘛 | `dalai-lama-perspective` | `references/perspectives/dalai-lama-perspective/PERSPECTIVE.md` | 第十四世达赖喇嘛的思维框架与表达方式。基于著作、访谈/文本、权威传记和外部评价的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用第十四世达赖喇嘛的视角分析慈悲、非暴力、世俗伦理、藏传佛教、流亡处境和跨宗教对话问题。 当用户提到「第十四世达赖喇嘛视角」「第十四世达赖喇嘛会怎么看」「… |
| 达尔文 | `darwin-perspective` | `references/perspectives/darwin-perspective/PERSPECTIVE.md` | 达尔文的思维框架与表达方式。基于著作、笔记、书信、航海经历和科学史研究的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用达尔文的视角分析进化、观察、证据、变异、适应、缓慢变化和科学论证。 当用户提到「达尔文视角」「达尔文会怎么看」「进化论」「自然选择」「物种起源」「适应」时使用。 |
| 爱因斯坦 | `einstein-perspective` | `references/perspectives/einstein-perspective/PERSPECTIVE.md` | 爱因斯坦的思维框架与表达方式。基于论文、书信、演讲、访谈、传记资料和科学史研究的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用爱因斯坦的视角分析物理直觉、思想实验、简单性、科学创造、和平主义和知识独立。 当用户提到「爱因斯坦视角」「爱因斯坦会怎么看」「思想实验」「相对论」「物理… |
| 理查德·费曼 | `feynman-perspective` | `references/perspectives/feynman-perspective/PERSPECTIVE.md` | 理查德·费曼的思维框架与表达方式。基于40+个一手来源的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用费曼的视角分析问题、审视决策、提供反馈。 当用户提到「用费曼的视角」「费曼会怎么看」「费曼模式」「feynman perspective」「费曼学习法」时使用。 即使用户… |
| 乔治·阿甘本 | `giorgio-agamben-perspective` | `references/perspectives/giorgio-agamben-perspective/PERSPECTIVE.md` | 乔治·阿甘本的思维框架与表达方式。基于 Homo Sacer（神圣人）系列、State of Exception（例外状态）、 The Coming Community（将来的共同体）、The Kingdom and the Glory（王国与荣耀）、出版社页面和权威资料， 提炼4个核心心智模型、7条决策启发式和表达… |
| 韩炳哲 | `byung-chul-han-perspective` | `references/perspectives/byung-chul-han-perspective/PERSPECTIVE.md` | 韩炳哲的思维框架与表达方式。基于 The Burnout Society（倦怠社会）、The Transparency Society（透明社会）、 Psychopolitics（心理政治）、The Scent of Time（时间的香气）、The Disappearance of Rituals（仪式的消失）等作品… |
| 昆汀·梅亚苏 | `quentin-meillassoux-perspective` | `references/perspectives/quentin-meillassoux-perspective/PERSPECTIVE.md` | 昆汀·梅亚苏的思维框架与表达方式。基于 After Finitude（有限性之后）、The Number and the Siren（数字与塞壬）、 Science Fiction and Extro-Science Fiction（科幻与外科学幻）、出版资料、大学资料和权威资料， 提炼4个核心心智模型、6条决策启发… |
| 格雷厄姆·哈曼 | `graham-harman-perspective` | `references/perspectives/graham-harman-perspective/PERSPECTIVE.md` | 格雷厄姆·哈曼（Graham Harman）公开视角卡；基于其对象导向本体论（Object-Oriented Ontology）著作、出版社资料、访谈和学术简介，提炼4个核心模型，适用于哲学建模、艺术/技术对象分析、反还原论判断；触发词：哈曼、格雷厄姆·哈曼、OOO、对象导向本体论、object-oriented o… |
| 康德 | `kant-perspective` | `references/perspectives/kant-perspective/PERSPECTIVE.md` | 康德的公开思维框架。外部领域：纯粹理性/道德律/批判哲学。从 Panmax/awesome-nuwa 的 Panmax/kant-skill 转换导入。 |
| 维特根斯坦 | `wittgenstein-perspective` | `references/perspectives/wittgenstein-perspective/PERSPECTIVE.md` | 维特根斯坦的公开思维框架。外部领域：语言哲学/逻辑/沉默。从 Panmax/awesome-nuwa 的 Panmax/wittgenstein-skill 转换导入。 |
| 西蒙娜·德·波伏娃 | `beauvoir-perspective` | `references/perspectives/beauvoir-perspective/PERSPECTIVE.md` | 西蒙娜·德·波伏娃的公开思维框架。外部领域：女性主义/存在主义/自由。从 Panmax/awesome-nuwa 的 Panmax/beauvoir-skill 转换导入。 |
| 赫拉利 | `harari-perspective` | `references/perspectives/harari-perspective/PERSPECTIVE.md` | 赫拉利的公开思维框架。外部领域：人类简史/未来/认知革命。从 Panmax/awesome-nuwa 的 Panmax/harari-skill 转换导入。 |

### 文学、艺术与电影（37 位）

| 中文/英文名 | Perspective | 路径 | 何时调用 |
|---|---|---|---|
| 罗伯特·布列松 | `robert-bresson-perspective` | `references/perspectives/robert-bresson-perspective/PERSPECTIVE.md` | 罗伯特·布列松的思维框架与表达方式。基于电影作品、《电影书写札记》、 访谈、Criterion/BFI/Cannes 等权威电影资料提炼。 用途：作为思维顾问，用布列松视角分析电影摄影术、声音、非职业表演、节制、剪辑、动作和精神性。 当用户提到「布列松视角」「电影书写札记」「电影摄影术」「模特」「扒手」「死囚越狱」「… |
| 让-吕克·戈达尔 | `jean-luc-godard-perspective` | `references/perspectives/jean-luc-godard-perspective/PERSPECTIVE.md` | 让-吕克·戈达尔的思维框架与表达方式。基于电影、访谈、电影著作、BFI、Criterion、Britannica 等公开资料提炼， 形成5个核心心智模型、7条启发式和表达DNA。 用途：作为思维顾问，用戈达尔视角分析电影语言、剪辑、政治形式、影像论文、媒介批判和作者创作问题。 当用户提到「戈达尔视角」「Godard … |
| 小津安二郎 | `yasujiro-ozu-perspective` | `references/perspectives/yasujiro-ozu-perspective/PERSPECTIVE.md` | 小津安二郎的思维框架与表达方式。基于电影、日记/访谈线索、剧作资料、BFI、Criterion、Britannica、MoMA/JFDB 等公开资料提炼， 形成5个核心心智模型、7条启发式和表达DNA。 用途：作为思维顾问，用小津视角分析家庭、日常、代际变化、静态构图、低机位、留白、节制和生活流逝。 当用户提到「小津… |
| 博尔赫斯 | `borges-perspective` | `references/perspectives/borges-perspective/PERSPECTIVE.md` | 博尔赫斯的思维框架与表达方式。基于小说、诗歌、随笔、访谈、自传材料和权威文学资料的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用博尔赫斯的视角分析文学、迷宫、无限、百科全书、镜像、时间、身份和虚构结构。 当用户提到「博尔赫斯视角」「博尔赫斯会怎么看」「迷宫」「巴别图书馆」「小径… |
| 卡夫卡 | `kafka-perspective` | `references/perspectives/kafka-perspective/PERSPECTIVE.md` | 卡夫卡的思维框架与表达方式。基于小说、短篇、日记、书信、传记资料和权威文学资料的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用卡夫卡的视角分析官僚程序、罪责、父权、异化、身体变形、门槛和现代主体困境。 当用户提到「卡夫卡视角」「卡夫卡会怎么看」「审判」「城堡」「变形记」「在法的… |
| 陈丹青 | `chen-danqing-perspective` | `references/perspectives/chen-danqing-perspective/PERSPECTIVE.md` | 陈丹青的思维框架与表达方式。基于著作、访谈/节目、公开资料和权威二手资料的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用陈丹青的视角分析艺术、哲学、文化和个人判断问题。 当用户提到「陈丹青视角」「陈丹青会怎么看」「陈丹青视角、局部、退步集、艺术教育、木心、美术馆、绘画观看」时使… |
| 戴锦华 | `dai-jinhua-perspective` | `references/perspectives/dai-jinhua-perspective/PERSPECTIVE.md` | 戴锦华的批评方法与问题意识。基于北大中文系资料、公开讲座、访谈、著作信息和外部评论的调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为文化批评、电影分析、性别研究和当代中国文化研究的思维顾问。 当用户提到「用戴锦华视角」「戴锦华会怎么看」「戴锦华式分析」「女性主义电影批评」「文化症候分析」时使用。 |
| 陀思妥耶夫斯基 | `dostoevsky-perspective` | `references/perspectives/dostoevsky-perspective/PERSPECTIVE.md` | 陀思妥耶夫斯基的思维框架与表达方式。基于小说、书信、《作家日记》、传记资料和外部批评的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用陀思妥耶夫斯基的视角分析文学、信仰、罪责、自由、人格撕裂和现代性问题。 当用户提到「陀思妥耶夫斯基视角」「陀氏会怎么看」「陀思妥耶夫斯基式分析」「… |
| 杜尚 | `duchamp-perspective` | `references/perspectives/duchamp-perspective/PERSPECTIVE.md` | 马塞尔·杜尚的思维框架与表达方式。基于现成品、访谈、笔记、作品说明、艺术史研究和外部批评的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用杜尚的视角分析艺术、制度、命名、选择、观看者、反品味和创作策略。 当用户提到「杜尚视角」「杜尚会怎么看」「现成品」「泉」「大玻璃」「反艺术」「… |
| 鲁迅 | `lu-xun-perspective` | `references/perspectives/lu-xun-perspective/PERSPECTIVE.md` | 鲁迅的思维框架与表达方式。基于著作、访谈/文本、权威传记和外部评价的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用鲁迅的视角分析现代文学、国民性批判、启蒙困境、杂文讽刺、沉默者和现代中国精神结构。 当用户提到「鲁迅视角」「鲁迅会怎么看」「鲁迅视角、国民性、铁屋子、呐喊、彷徨、杂… |
| 塔可夫斯基 | `tarkovsky-perspective` | `references/perspectives/tarkovsky-perspective/PERSPECTIVE.md` | 安德烈·塔可夫斯基的思维框架与表达方式。基于电影、著作《雕刻时光》、日记、访谈、创作记录和外部批评的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用塔可夫斯基的视角分析电影、时间、精神经验、影像伦理、牺牲和作者创作。 当用户提到「塔可夫斯基视角」「塔可夫斯基会怎么看」「雕刻时光」… |
| 梵高 | `van-gogh-perspective` | `references/perspectives/van-gogh-perspective/PERSPECTIVE.md` | 梵高的思维框架与表达方式。基于著作、访谈/文本、权威传记和外部评价的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用梵高的视角分析绘画、色彩、艺术使命、贫困、孤独、劳动、精神痛苦和创作坚持问题。 当用户提到「梵高视角」「梵高会怎么看」「梵高视角、向日葵、星夜、书信、色彩、后印象派… |
| 瓦尔特·本雅明 | `walter-benjamin-perspective` | `references/perspectives/walter-benjamin-perspective/PERSPECTIVE.md` | 瓦尔特·本雅明的思维框架与表达方式。基于论文、札记、《拱廊计划》、书信、传记资料和外部研究的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用本雅明的视角分析现代性、影像、复制技术、灵韵、城市、废墟、档案和历史哲学。 当用户提到「本雅明视角」「本雅明会怎么看」「灵韵」「机械复制」「… |
| 王家卫 | `wong-kar-wai-perspective` | `references/perspectives/wong-kar-wai-perspective/PERSPECTIVE.md` | 王家卫的思维框架与表达方式。基于著作、访谈/文本、权威传记和外部评价的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用王家卫的视角分析电影、时间、都市情感、错过、香港经验、音乐与影像风格问题。 当用户提到「王家卫视角」「王家卫会怎么看」「王家卫视角、重庆森林、花样年华、阿飞正传、… |
| 毛泽东 | `mao-zedong-perspective` | `references/perspectives/mao-zedong-perspective/PERSPECTIVE.md` | 毛泽东的思维框架与表达方式。基于著作、访谈/文本、权威传记和外部评价的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用毛泽东的视角分析矛盾论、实践论、群众路线、持久战、组织动员和现代中国历史问题。 当用户提到「毛泽东视角」「毛泽东会怎么看」「毛泽东视角、矛盾论、实践论、群众路线、… |
| 阿彼察邦·韦拉斯哈古 | `apichatpong-weerasethakul-perspective` | `references/perspectives/apichatpong-weerasethakul-perspective/PERSPECTIVE.md` | 阿彼察邦·韦拉斯哈古的影像、梦、记忆与政治感知视角。基于公开材料推断，非本人观点。 提炼4个核心心智模型、7条决策启发式和表达DNA；适用于慢电影、装置影像、梦境叙事、地方记忆、审查与感知政治分析。 触发词：阿彼察邦视角、Weerasethakul、热带疾病、能召回前世的布米叔叔、记忆、梦、丛林、幽灵、缓慢电影。 |
| 佩德罗·科斯塔 | `pedro-costa-perspective` | `references/perspectives/pedro-costa-perspective/PERSPECTIVE.md` | 佩德罗·科斯塔的房间、贫困、暗部、移民记忆与电影伦理视角。基于公开材料推断，非本人观点。 提炼4个核心心智模型、7条决策启发式和表达DNA；适用于丰泰尼亚斯、数字影像、非职业演员、贫困再现、电影伦理与慢电影分析。 触发词：Pedro Costa、佩德罗科斯塔、丰泰尼亚斯、凡达的房间、青春向前行、马钱、维塔莉娜·瓦雷拉… |
| 大卫·林奇 | `david-lynch-perspective` | `references/perspectives/david-lynch-perspective/PERSPECTIVE.md` | 大卫·林奇的梦逻辑、潜意识、美国表层裂缝、声音与图像炼金术视角。基于公开材料推断，非本人观点。 林奇已于2025年1月去世，但仍塑造21世纪精神图景；本卡提炼4个核心心智模型、7条决策启发式和表达DNA。 适用于电影、电视剧、梦境叙事、恐惧美学、声音设计、创意直觉与美国文化阴影分析。 |
| 贝拉·塔尔 | `bela-tarr-perspective` | `references/perspectives/bela-tarr-perspective/PERSPECTIVE.md` | 贝拉·塔尔的思维框架与表达方式。基于匈牙利国家电影资料、Sarajevo Film Academy/Film Factory、 访谈、影展资料和权威评论，提炼4个核心心智模型、7条决策启发式和表达DNA。 用途：作为创作与判断顾问，用塔尔视角分析时间、贫困、命运、长镜头、环境伦理和电影中的存在状态。 当用户提到「贝拉… |
| 蔡明亮 | `tsai-ming-liang-perspective` | `references/perspectives/tsai-ming-liang-perspective/PERSPECTIVE.md` | 蔡明亮的思维框架与表达方式。基于台湾电影资料库、威尼斯双年展、MoMA/Walker等机构资料、 访谈与作品线索，提炼4个核心心智模型、7条决策启发式和表达DNA。 用途：作为创作与判断顾问，用蔡明亮视角分析身体、孤独、城市空间、凝视、慢速时间和电影/美术馆边界。 当用户提到「蔡明亮视角」「Tsai Ming-lia… |
| 卡洛斯·雷加达斯 | `carlos-reygadas-perspective` | `references/perspectives/carlos-reygadas-perspective/PERSPECTIVE.md` | 卡洛斯·雷加达斯的思维框架与表达方式。基于 Cannes、Morelia、Indiana Cinema、BAMPFA、 Criterion 等机构资料、访谈和作品线索，提炼4个核心心智模型、7条决策启发式和表达DNA。 用途：作为创作与判断顾问，用 Reygadas 视角分析感官现实、非职业演员、自然光、身体、信仰、… |
| 黑特·史德耶尔 | `hito-steyerl-perspective` | `references/perspectives/hito-steyerl-perspective/PERSPECTIVE.md` | 黑特·史德耶尔（Hito Steyerl）公开视角卡；基于其艺术家/影像作品、e-flux文章、出版社资料、美术馆资料和访谈，提炼4个核心模型，适用于图像政治、数字平台、艺术制度、AI与战争媒介分析；触发词：Hito Steyerl、黑特·史德耶尔、poor image、Duty Free Art、图像政治。 |
| 阿尔沃·帕尔特 | `arvo-part-perspective` | `references/perspectives/arvo-part-perspective/PERSPECTIVE.md` | 阿尔沃·帕尔特的思维框架与表达方式。基于 Arvo Part Centre、ECM、出版资料、访谈与权威音乐机构资料提炼， 形成4个核心心智模型、7条决策启发式和表达DNA。 用途：作为思维顾问，用帕尔特视角分析极简、神圣音乐、沉默、tintinnabuli（钟鸣作曲法）、创作克制和精神时间问题。 当用户提到「帕尔特… |
| 布莱恩·伊诺 | `brian-eno-perspective` | `references/perspectives/brian-eno-perspective/PERSPECTIVE.md` | 布莱恩·伊诺的思维框架与表达方式。基于 brian-eno.net、Oblique Strategies、Long Now、出版资料、访谈和权威音乐资料提炼， 形成5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用伊诺视角分析生成系统、ambient（环境音乐）、工作室实验、限制策略、艺术技术和文… |
| 威廉·巴辛斯基 | `william-basinski-perspective` | `references/perspectives/william-basinski-perspective/PERSPECTIVE.md` | 威廉·巴辛斯基的思维框架与表达方式。基于 2062 官方资料、Temporary Residence、The Disintegration Loops 相关访谈、厂牌和权威媒体资料提炼， 形成4个核心心智模型、7条决策启发式和表达DNA。 用途：作为思维顾问，用巴辛斯基视角分析磁带衰变、记忆、循环、档案、灾难余波、声… |
| 池田亮司 | `ryoji-ikeda-perspective` | `references/perspectives/ryoji-ikeda-perspective/PERSPECTIVE.md` | 池田亮司的思维框架与表达方式。基于官方作品页、传记、展览资料、访谈和艺术机构资料提炼。 用途：作为视听、数据美学和极限感知顾问，用于分析声音/光/数学/数据/沉浸装置/极简电子音乐。 触发词：池田亮司、Ryoji Ikeda、data-verse、datamatics、test pattern、spectra、数据美… |
| 蒂姆·赫克 | `tim-hecker-perspective` | `references/perspectives/tim-hecker-perspective/PERSPECTIVE.md` | 蒂姆·赫克的思维框架与表达方式。基于官网、厂牌资料、唱片项目、访谈和权威音乐媒体资料提炼。 用途：作为声音、噪声、衰败介质、后数字氛围和反高清美学顾问，用于分析实验电子音乐、声音设计、空间声场和创作策略。 触发词：Tim Hecker、蒂姆·赫克、Ravedeath 1972、Harmony in Ultraviol… |
| 约恩·福瑟 | `jon-fosse-perspective` | `references/perspectives/jon-fosse-perspective/PERSPECTIVE.md` | 约恩·福瑟的思维框架与表达方式。基于诺奖官方资料、出版社资料、作品目录、诺奖演讲和权威文学资料提炼。 用途：作为极简文学、戏剧、沉默、重复、信仰边界和存在经验顾问，用于分析写作、剧场、叙事节奏和精神性表达。 触发词：Jon Fosse、约恩·福瑟、Septology、A New Name、Melancholy、Som… |
| 奥尔加·托卡尔丘克 | `olga-tokarczuk-perspective` | `references/perspectives/olga-tokarczuk-perspective/PERSPECTIVE.md` | 奥尔加·托卡尔丘克（Olga Tokarczuk）公开视角卡；基于诺贝尔官方资料、诺奖演讲、出版社资料和权威访谈，提炼4个核心模型，适用于小说结构、叙事伦理、生态想象、跨边界人物与世界建构；触发词：托卡尔丘克、奥尔加·托卡尔丘克、Olga Tokarczuk、Tender Narrator、云游派。 |
| 托马斯·品钦 | `thomas-pynchon-perspective` | `references/perspectives/thomas-pynchon-perspective/PERSPECTIVE.md` | 托马斯·品钦的思维框架与表达方式。基于出版社、奖项机构、百科资料和作品出版信息的初版调研， 提炼4个核心心智模型、7条决策启发式和表达DNA。 用途：作为文学、系统、阴谋、技术官僚制、熵、美国历史和后现代叙事问题的分析视角。 当用户提到「品钦视角」「Pynchon会怎么看」「托马斯·品钦、万有引力之虹、拍卖第49批、… |
| 安藤忠雄 | `tadao-ando-perspective` | `references/perspectives/tadao-ando-perspective/PERSPECTIVE.md` | 安藤忠雄的思维框架与表达方式。基于普利兹克奖、博物馆/艺术机构、建筑项目资料和公开机构页面的初版调研， 提炼4个核心心智模型、7条决策启发式和表达DNA。 用途：作为建筑、空间、光、混凝土、自然、修行式创作和场所精神问题的分析视角。 当用户提到「安藤忠雄视角」「Ando会怎么看」「清水混凝土、光之教堂、住吉长屋、直岛… |
| 雷姆·库哈斯 | `rem-koolhaas-perspective` | `references/perspectives/rem-koolhaas-perspective/PERSPECTIVE.md` | 雷姆·库哈斯的思维框架与表达方式。基于 OMA、普利兹克奖、建筑项目页面和机构资料的初版调研， 提炼4个核心心智模型、8条决策启发式和表达DNA。 用途：作为城市、建筑、现代化、拥挤、项目研究、矛盾、基础设施和全球化空间问题的分析视角。 当用户提到「库哈斯视角」「Koolhaas会怎么看」「OMA、癫狂纽约、S,M,… |
| 彼得·卒姆托 | `peter-zumthor-perspective` | `references/perspectives/peter-zumthor-perspective/PERSPECTIVE.md` | 彼得·卒姆托的建筑思维框架与表达方式。基于普利兹克奖、出版社、建筑项目与权威机构资料， 提炼4个核心心智模型、7条决策启发式和完整表达DNA。 用途：作为思维顾问，用卒姆托视角分析空间、材料、场所、慢工与设计取舍。 当用户提到「卒姆托视角」「Zumthor perspective」「建筑氛围」「材料真实」「Therm… |
| 内里·奥克斯曼 | `neri-oxman-perspective` | `references/perspectives/neri-oxman-perspective/PERSPECTIVE.md` | 内里·奥克斯曼的设计、材料与生物制造思维框架。基于 MIT、MoMA、MIT Press、OXMAN 与权威报道资料， 提炼4个核心心智模型、7条决策启发式和完整表达DNA。 用途：作为思维顾问，用奥克斯曼视角分析材料生态、设计工程、生物制造、跨学科工作流与伦理边界。 当用户提到「奥克斯曼视角」「Neri Oxman… |
| 罗伯特·麦基 | `mckee-perspective` | `references/perspectives/mckee-perspective/PERSPECTIVE.md` | 罗伯特·麦基的公开思维框架。外部领域：故事结构/编剧方法论/叙事原理。从 Panmax/awesome-nuwa 的 Panmax/mckee-skill 转换导入。 |
| 宫崎骏 | `miyazaki-perspective` | `references/perspectives/miyazaki-perspective/PERSPECTIVE.md` | 宫崎骏的公开思维框架。外部领域：动画/自然/想象力。从 Panmax/awesome-nuwa 的 Panmax/miyazaki-skill 转换导入。 |
| 黑泽明 | `kurosawa-perspective` | `references/perspectives/kurosawa-perspective/PERSPECTIVE.md` | 黑泽明的公开思维框架。外部领域：电影/叙事/完美主义。从 Panmax/awesome-nuwa 的 Panmax/kurosawa-skill 转换导入。 |

### 政治、战略与历史（1 位）

| 中文/英文名 | Perspective | 路径 | 何时调用 |
|---|---|---|---|
| 李光耀 | `liguangyao-perspective` | `references/perspectives/liguangyao-perspective/PERSPECTIVE.md` | 李光耀的公开思维框架。外部领域：治国/实用主义/制度设计。从 Panmax/awesome-nuwa 的 Panmax/liguangyao-skill 转换导入。 |

### 闲聊酒馆（6 位）

| 中文/英文名 | Perspective | 路径 | 何时调用 |
|---|---|---|---|
| 迈克尔·杰克逊 | `michael-jackson-perspective` | `references/tavern/michael-jackson-perspective/PERSPECTIVE.md` | 迈克尔·杰克逊的创作与表演系统。基于专辑、演出影像、访谈、制作记录、传记资料和外部评论的初版调研， 提炼5个核心心智模型、8条决策启发式和表达DNA。 用途：作为思维顾问，用迈克尔·杰克逊的视角分析舞台、节奏、声音、身体控制、流行音乐工业、公众形象和创作纪律。 当用户提到「迈克尔杰克逊视角」「MJ会怎么看」「流行音乐… |
| 太宰治 | `dazai-perspective` | `references/tavern/dazai-perspective/PERSPECTIVE.md` | 太宰治的公开思维框架。外部领域：人间失格/边缘人视角/自我解剖。从 Panmax/awesome-nuwa 的 Panmax/dazai-skill 转换导入。 |
| 王小波 | `wangxiaobo-perspective` | `references/tavern/wangxiaobo-perspective/PERSPECTIVE.md` | 王小波的公开思维框架。外部领域：自由/理性/黑色幽默。从 Panmax/awesome-nuwa 的 Panmax/wangxiaobo-skill 转换导入。 |
| 张雪峰 | `zhangxuefeng-perspective` | `references/tavern/zhangxuefeng-perspective/PERSPECTIVE.md` | 张雪峰的思维框架与表达方式。基于5本著作、15+篇权威媒体深度采访、 30+条一手语录、11个关键决策记录和完整人生时间线的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用张雪峰的视角分析教育选择、职业规划、阶层流动等问题。 当用户提到「用张雪峰的视角」「张雪峰会怎么看」「… |
| 特朗普 | `trump-perspective` | `references/tavern/trump-perspective/PERSPECTIVE.md` | 唐纳德·特朗普（Donald Trump）的思维框架与行为逻辑。基于著作、长访谈、辩论、 心理分析、前幕僚回忆录、重大决策记录共6个维度的深度调研（320KB+原始资料）， 提炼6个核心心智模型、8条决策启发式和完整的表达DNA。 用途：（1）思维顾问——用特朗普视角分析谈判、权力、传播问题； （2）行为预判——解读… |
| 孙宇晨 | `sun-yuchen-perspective` | `references/tavern/sun-yuchen-perspective/PERSPECTIVE.md` | 孙宇晨（Justin Sun / 孙割）的思维框架与行为逻辑。基于6个维度（著作、深度采访、表达DNA、 他者视角、决策记录、时间线）共1500+行调研素材的深度蒸馏， 提炼6个核心心智模型、8条决策启发式、5种割味造句公式和完整的表达DNA。 用途：作为思维顾问，用孙宇晨的视角分析营销策略、注意力经济、危机公关、叙… |
