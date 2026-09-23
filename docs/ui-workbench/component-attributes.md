# 组件属性实测附表（V3.1）

由tools/build-ui-reference.py从computed-ui.json生成。默认风格；D=1440×900，M=390×844；所有长度为CSS px。W×H是本次文案/字体下的实际包围盒，不应全部硬编码。P/M=padding/margin，顺序为上右下左（CSS简写）；gap列可能为normal，表示未显式指定，不能理解为组件无间隔。

本表覆盖常用代表组件；同类不同位置、选中/异常状态、全部边框/阴影/滚动/定位属性查JSON。定位名称对应原型，不代表正式业务页面已补齐。

|组件 / 场景 / 选择器|视口|W×H|字号 / 字重 / 行高|P；M；gap|圆角 / 边框|前景 / 背景|
|---|---|---|---|---|---|---|
|工作台侧栏 / overview / `.sidebar`|D|216.00×900.00|15px / 400 / 24.75px|28px 15px 16px；0px；normal|0px / |rgb(36, 46, 43) / rgb(255, 254, 250)|
|顶部栏 / overview / `.work-header`|D|1224.00×76.00|15px / 400 / 24.75px|12px 36px；0px；16px|0px / |rgb(36, 46, 43) / rgb(255, 254, 250)|
|顶部栏 / overview / `.work-header`|M|390.00×64.00|15px / 400 / 24.75px|10px 16px；0px；16px|0px / |rgb(36, 46, 43) / rgb(255, 254, 250)|
|头部操作组 / overview / `.work-header-actions`|D|249.56×40.00|15px / 400 / 24.75px|0px；0px；16px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|头部操作组 / overview / `.work-header-actions`|M|157.28×40.00|15px / 400 / 24.75px|0px；0px；5px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|主体滚动区 / overview / `#work-main`|D|1224.00×781.86|15px / 400 / 24.75px|30px 36px 24px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|主体滚动区 / overview / `#work-main`|M|390.00×718.00|15px / 400 / 24.75px|22px 16px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|侧栏菜单 / overview / `.side-nav button`|D|185.00×46.00|14px / 600 / 20.3px|11px 14px；0px；12px|7px / 1px solid rgba(0, 0, 0, 0)|rgb(146, 63, 48) / rgb(243, 233, 227)|
|侧栏品牌 / overview / `.work-brand`|D|185.00×56.39|22px / 600 / 30.8px|0px 10px；0px；12px|7px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|品牌印章 / overview / `.brand-seal`|D|38.00×40.00|25px / 500 / 25px|0px；0px；normal|6px / 1px solid rgb(172, 101, 85)|rgb(255, 247, 233) / rgb(146, 63, 48)|
|移动导航 / overview / `.mobile-nav`|M|390.00×62.00|15px / 400 / 24.75px|5px 12px；0px；normal|0px / |rgb(36, 46, 43) / rgb(255, 254, 250)|
|移动导航按钮 / overview / `.mobile-nav button`|M|91.50×51.00|11px / 500 / 15.95px|5px；0px；4px|7px / 0px none rgb(146, 63, 48)|rgb(146, 63, 48) / rgb(246, 238, 232)|
|移动导航图标 / overview / `.mobile-nav i`|M|21.00×21.00|21px / 500 / 21px|0px；0px；normal|0px / 0px none rgb(146, 63, 48)|rgb(146, 63, 48) / rgba(0, 0, 0, 0)|
|首页标题 / overview / `.welcome h1`|D|1152.00×42.00|28px / 500 / 42px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|首页标题 / overview / `.welcome h1`|M|358.00×37.50|25px / 500 / 37.5px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|首页副标题 / overview / `.welcome p`|D|1152.00×23.09|14px / 400 / 23.1px|0px；8px 0px 0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|首页副标题 / overview / `.welcome p`|M|280.00×23.39|13px / 400 / 23.4px|0px；8px 0px 0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|首页眉题 / overview / `.eyebrow`|D|1152.00×18.14|11px / 400 / 18.15px|0px；0px 0px 7px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|首页眉题 / overview / `.eyebrow`|M|358.00×16.50|10px / 400 / 16.5px|0px；0px 0px 7px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|提出需求卡 / overview / `.start-card`|D|1152.00×165.44|15px / 400 / 24.75px|26px 28px；0px 0px 26px；22px|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|提出需求卡 / overview / `.start-card`|M|358.00×154.59|15px / 400 / 24.75px|21px 18px；0px 0px 20px；12px|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|提出需求标题 / overview / `.start-copy h2`|D|742.00×27.00|18px / 600 / 27px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|提出需求标题 / overview / `.start-copy h2`|M|274.00×24.00|16px / 600 / 24px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|提出需求主按钮 / overview / `.start-copy button`|D|107.00×40.00|13px / 500 / 18.85px|8px 14px；0px；7px|7px / 1px solid rgb(146, 63, 48)|rgb(255, 254, 250) / rgb(146, 63, 48)|
|提出需求主按钮 / overview / `.start-copy button`|M|93.00×42.00|12px / 500 / 17.4px|9px 10px；0px；7px|7px / 1px solid rgb(146, 63, 48)|rgb(255, 254, 250) / rgb(146, 63, 48)|
|概览两栏 / overview / `.overview-columns`|D|1152.00×734.55|15px / 400 / 24.75px|0px；0px；24px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|概览两栏 / overview / `.overview-columns`|M|358.00×1633.50|15px / 400 / 24.75px|0px；0px；18px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|最近事项卡 / overview / `.recent-card`|D|828.00×629.75|15px / 400 / 24.75px|22px 24px 0px；0px；normal|11px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|最近事项卡 / overview / `.recent-card`|M|358.00×721.89|15px / 400 / 24.75px|18px 16px 0px；0px；normal|11px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|卡片标题 / overview / `.section-head h2`|D|204.00×24.00|16px / 600 / 24px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|卡片标题 / overview / `.section-head h2`|M|187.00×22.50|15px / 600 / 22.5px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|事项行 / overview / `.task-row`|D|778.00×89.39|15px / 400 / 24.75px|17px 0px；0px；12px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|事项行 / overview / `.task-row`|M|324.00×109.25|15px / 400 / 24.75px|17px 0px；0px；9px 8px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|事项名 / overview / `.task-title`|D|148.67×23.25|15px / 500 / 23.25px|0px；0px 0px 7px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|事项名 / overview / `.task-title`|M|324.00×23.25|15px / 500 / 23.25px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|事项元信息 / overview / `.task-meta`|D|148.67×24.14|12px / 400 / 19.8px|0px；0px；9px|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|事项元信息 / overview / `.task-meta`|M|244.00×24.14|11px / 400 / 18.15px|0px；0px；5px|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|状态标签 / overview / `.status`|D|57.00×24.14|11px / 500 / 18.15px|3px 7px；0px；5px|4px / 0px none rgb(33, 96, 77)|rgb(33, 96, 77) / rgb(234, 242, 237)|
|状态标签 / overview / `.status`|M|55.00×24.14|11px / 500 / 18.15px|3px 6px；0px；5px|4px / 0px none rgb(33, 96, 77)|rgb(33, 96, 77) / rgb(234, 242, 237)|
|页签 / overview / `.tabs button`|D|68.00×44.00|13px / 500 / 18.85px|12px 8px；0px；7px|0px / 0px none rgb(146, 63, 48)|rgb(146, 63, 48) / rgba(0, 0, 0, 0)|
|页签 / overview / `.tabs button`|M|58.00×44.00|12px / 500 / 17.4px|12px 5px；0px；7px|0px / 0px none rgb(146, 63, 48)|rgb(146, 63, 48) / rgba(0, 0, 0, 0)|
|地图预览卡 / overview / `.map-entry`|D|300.00×176.00|14px / 500 / 20.3px|0px；0px；7px|11px / 1px solid rgb(202, 199, 181)|rgb(255, 249, 233) / rgba(0, 0, 0, 0)|
|地图预览卡 / overview / `.map-entry`|M|358.00×185.00|14px / 500 / 20.3px|0px；0px；7px|11px / 1px solid rgb(202, 199, 181)|rgb(255, 249, 233) / rgba(0, 0, 0, 0)|
|侧边好汉头像 / overview / `.compact-agent .portrait`|D|36.00×36.00|14px / 500 / 20.3px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|侧边好汉头像 / overview / `.compact-agent .portrait`|M|40.00×40.00|14px / 500 / 20.3px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|资料条 / overview / `.resource-strip`|D|828.00×84.80|15px / 400 / 24.75px|19px 22px；0px；14px|11px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|资料条 / overview / `.resource-strip`|M|358.00×117.28|15px / 400 / 24.75px|18px 16px；0px；12px|11px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|普通页面眉题 / bounty / `.page-heading .eyebrow`|D|1152.00×18.14|11px / 400 / 18.15px|0px；0px 0px 8px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|普通页面眉题 / bounty / `.page-heading .eyebrow`|M|358.00×18.14|11px / 400 / 18.15px|0px；0px 0px 8px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|普通页面标题 / bounty / `#page-title`|D|1152.00×37.80|27px / 500 / 37.8px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|普通页面标题 / bounty / `#page-title`|M|358.00×35.00|25px / 500 / 35px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|普通页面说明 / bounty / `#page-description`|D|1152.00×23.09|14px / 400 / 23.1px|0px；8px 0px 0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|普通页面说明 / bounty / `#page-description`|M|358.00×23.39|13px / 400 / 23.4px|0px；8px 0px 0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|普通页面容器 / bounty / `.page-surface`|D|1152.00×763.77|15px / 400 / 24.75px|0px；0px；normal|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|普通页面容器 / bounty / `.page-surface`|M|358.00×927.03|15px / 400 / 24.75px|0px；0px；normal|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|普通页面内边距 / bounty / `#page-body`|D|1150.00×761.77|15px / 400 / 24.75px|26px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|普通页面内边距 / bounty / `#page-body`|M|356.00×925.03|15px / 400 / 24.75px|20px 16px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|筛选行 / bounty / `.filter-row`|D|1098.00×42.00|15px / 400 / 24.75px|0px；0px 0px 18px；12px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|筛选行 / bounty / `.filter-row`|M|324.00×144.00|15px / 400 / 24.75px|0px；0px 0px 18px；12px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|本领下拉 / bounty / `#ability-filter`|D|190.00×40.00|14px / 400 / normal|7px 10px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|本领下拉 / bounty / `#ability-filter`|M|324.00×40.00|14px / 400 / normal|7px 10px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|事项搜索输入 / bounty / `#task-query`|D|1003.00×48.39|16px / 400 / 26.4px|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|事项搜索输入 / bounty / `#task-query`|M|229.00×48.39|16px / 400 / 26.4px|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|榜文标题 / bounty / `.task-title`|D|155.56×24.80|16px / 500 / 24.8px|0px；0px 0px 7px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|榜文标题 / bounty / `.task-title`|M|324.00×23.25|15px / 500 / 23.25px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|榜文操作按钮 / bounty / `.task-actions button`|D|105.00×36.84|13px / 500 / 18.85px|8px 14px；0px；7px|7px / 1px solid rgb(227, 229, 220)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|榜文操作按钮 / bounty / `.task-actions button`|M|83.00×42.00|11px / 500 / 15.95px|8px；0px；7px|7px / 1px solid rgb(227, 229, 220)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|弹层总框 / demand / `#panel`|D|720.00×836.00|15px / 400 / 24.75px|0px；32px 360px；normal|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|弹层总框 / demand / `#panel`|M|390.00×844.00|15px / 400 / 24.75px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|弹层页头 / demand / `.panel-header`|D|718.00×94.94|15px / 400 / 24.75px|21px 26px；0px；12px|0px / |rgb(36, 46, 43) / rgb(255, 254, 250)|
|弹层页头 / demand / `.panel-header`|M|390.00×81.89|15px / 400 / 24.75px|16px；0px；12px|0px / |rgb(36, 46, 43) / rgb(255, 254, 250)|
|弹层眉题 / demand / `.panel-kicker`|D|96.78×18.14|11px / 400 / 18.15px|0px；0px 0px 3px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|弹层眉题 / demand / `.panel-kicker`|M|88.89×16.50|10px / 400 / 16.5px|0px；0px 0px 3px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|弹层标题 / demand / `#panel-title`|D|96.78×30.80|22px / 500 / 30.8px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|弹层标题 / demand / `#panel-title`|M|88.89×29.39|21px / 500 / 29.4px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|弹层正文区 / demand / `#panel-body`|D|718.00×662.06|15px / 400 / 24.75px|26px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|弹层正文区 / demand / `#panel-body`|M|390.00×689.11|15px / 400 / 24.75px|20px 16px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|弹层页脚 / demand / `#panel-footer`|D|718.00×77.00|15px / 400 / 24.75px|16px 24px；0px；12px|0px / |rgb(36, 46, 43) / rgb(245, 244, 240)|
|弹层页脚 / demand / `#panel-footer`|M|390.00×73.00|15px / 400 / 24.75px|14px 16px；0px；8px|0px / |rgb(36, 46, 43) / rgb(245, 244, 240)|
|需求步骤条 / demand / `.steps`|D|666.00×42.00|13px / 400 / 21.45px|0px 0px 18px；0px 0px 24px；18px|0px / |rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|需求步骤条 / demand / `.steps`|M|358.00×42.00|13px / 400 / 21.45px|0px 0px 18px；0px 0px 22px；16px|0px / |rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|表单字段组 / demand / `.field`|D|666.00×105.28|15px / 400 / 24.75px|0px；0px 0px 20px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|表单字段组 / demand / `.field`|M|358.00×105.28|15px / 400 / 24.75px|0px；0px 0px 19px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|字段标签 / demand / `.field-label`|D|666.00×23.09|14px / 600 / 23.1px|0px；0px 0px 8px；10px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|字段标签 / demand / `.field-label`|M|358.00×23.09|14px / 600 / 23.1px|0px；0px 0px 8px；10px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|单行输入 / demand / `.field input`|D|666.00×48.39|16px / 400 / 26.4px|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|单行输入 / demand / `.field input`|M|358.00×48.39|16px / 400 / 26.4px|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|需求多行输入 / demand / `.field textarea`|D|666.00×128.00|16px / 400 / 27.2px|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|需求多行输入 / demand / `.field textarea`|M|358.00×116.00|16px / 400 / 27.2px|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|字段辅助 / demand / `.field-help`|D|666.00×19.80|12px / 400 / 19.8px|0px；6px 0px 0px；12px|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|字段辅助 / demand / `.field-help`|M|358.00×19.80|12px / 400 / 19.8px|0px；6px 0px 0px；12px|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|附件选择区 / demand / `.upload-block`|D|666.00×70.00|15px / 400 / 24.75px|13px；0px；12px|6px / 1px dashed rgb(197, 204, 188)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|附件选择区 / demand / `.upload-block`|M|358.00×68.00|15px / 400 / 24.75px|12px；0px；8px|6px / 1px dashed rgb(197, 204, 188)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|附件chip / demand / `.attachment-chip`|D|118.34×37.44|13px / 400 / 21.45px|7px 10px；0px；7px|5px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(240, 242, 233)|
|附件chip / demand / `.attachment-chip`|M|118.34×37.44|13px / 400 / 21.45px|7px 10px；0px；7px|5px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(240, 242, 233)|
|字段错误 / demand-error / `#demand-error`|D|666.00×21.44|13px / 400 / 21.45px|0px；8px 0px；normal|0px / 0px none rgb(161, 63, 53)|rgb(161, 63, 53) / rgba(0, 0, 0, 0)|
|字段错误 / demand-error / `#demand-error`|M|358.00×21.44|13px / 400 / 21.45px|0px；8px 0px；normal|0px / 0px none rgb(161, 63, 53)|rgb(161, 63, 53) / rgba(0, 0, 0, 0)|
|确认说明 / confirm / `.notice`|D|666.00×46.09|13px / 400 / 22.1px|12px 14px；0px；normal|6px / |rgb(93, 102, 89) / rgb(242, 242, 234)|
|确认说明 / confirm / `.notice`|M|358.00×68.19|13px / 400 / 22.1px|12px 14px；0px；normal|6px / |rgb(93, 102, 89) / rgb(242, 242, 234)|
|详情定义列表 / confirm / `.definition`|D|666.00×95.28|14px / 400 / 23.1px|0px；0px；13px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|详情定义列表 / confirm / `.definition`|M|358.00×93.28|14px / 400 / 23.1px|0px；0px；12px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|明确好汉下拉 / confirm / `#assign-agent`|D|666.00×44.00|16px / 400 / normal|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|明确好汉下拉 / confirm / `#assign-agent`|M|358.00×44.00|16px / 400 / normal|10px 12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|空列表 / bounty-empty / `.empty`|D|1098.00×217.09|15px / 400 / 24.75px|48px 20px；0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|空列表 / bounty-empty / `.empty`|M|324.00×217.09|15px / 400 / 24.75px|48px 20px；0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|好汉双栏 / agent-selected / `.agent-layout`|D|1098.00×386.25|15px / 400 / 24.75px|0px；20px 0px 0px；24px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|好汉双栏 / agent-selected / `.agent-layout`|M|324.00×754.36|15px / 400 / 24.75px|0px；20px 0px 0px；16px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|好汉选中行 / agent-selected / `.selected`|D|626.48×90.56|14px / 500 / 20.3px|12px；0px；12px|7px / 1px solid rgb(165, 185, 153)|rgb(36, 46, 43) / rgb(237, 243, 233)|
|好汉选中行 / agent-selected / `.selected`|M|324.00×107.75|14px / 500 / 20.3px|11px；0px；10px|7px / 1px solid rgb(165, 185, 153)|rgb(36, 46, 43) / rgb(237, 243, 233)|
|好汉列表头像 / agent-selected / `.agent-row .portrait`|D|44.00×44.00|14px / 500 / 20.3px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|好汉列表头像 / agent-selected / `.agent-row .portrait`|M|44.00×44.00|14px / 500 / 20.3px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|好汉详情头像 / agent-selected / `.agent-detail .portrait`|D|76.00×76.00|15px / 400 / 24.75px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|好汉详情头像 / agent-selected / `.agent-detail .portrait`|M|76.00×76.00|15px / 400 / 24.75px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|好汉详情 / agent-selected / `.agent-detail`|D|447.50×344.92|15px / 400 / 24.75px|20px；0px；normal|8px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(250, 251, 246)|
|好汉详情 / agent-selected / `.agent-detail`|M|324.00×340.92|15px / 400 / 24.75px|18px；0px；normal|8px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(250, 251, 246)|
|文件网格 / files / `.file-grid`|D|1098.00×330.88|15px / 400 / 24.75px|0px；18px 0px 0px；12px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|文件网格 / files / `.file-grid`|M|324.00×478.31|15px / 400 / 24.75px|0px；18px 0px 0px；12px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|文件卡片 / files / `.file-card`|D|543.00×159.44|15px / 400 / 24.75px|22px；0px；normal|7px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|文件卡片 / files / `.file-card`|M|324.00×151.44|15px / 400 / 24.75px|18px；0px；normal|7px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|文件操作按钮 / files / `.file-card button`|D|46.00×40.00|13px / 500 / 18.85px|6px 9px；0px；7px|7px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|文件操作按钮 / files / `.file-card button`|M|46.00×40.00|13px / 500 / 18.85px|6px 9px；0px；7px|7px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|资料选择项 / materials / `.check-row`|D|946.00×75.19|14px / 400 / 23.1px|14px 0px；0px；12px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|资料选择项 / materials / `.check-row`|M|358.00×75.19|14px / 400 / 23.1px|14px 0px；0px；12px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|文档预览 / preview / `.document-preview`|D|680.00×336.69|15px / 400 / 24.75px|24px；0px 133px；normal|8px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|文档预览 / preview / `.document-preview`|M|358.00×328.69|15px / 400 / 24.75px|20px；0px；normal|8px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|典籍目录行 / archive / `.doc-row`|D|1098.00×81.03|14px / 500 / 20.3px|18px 0px；0px；14px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|典籍目录行 / archive / `.doc-row`|M|324.00×81.03|14px / 500 / 20.3px|18px 0px；0px；14px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|阅读弹层 / reader / `#panel`|D|1000.00×685.58|15px / 400 / 24.75px|0px；107.203px 220px 107.219px；normal|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|阅读弹层 / reader / `#panel`|M|390.00×844.00|15px / 400 / 24.75px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|阅读正文容器 / reader / `.reader`|D|680.00×459.64|16px / 400 / 30.4px|12px 0px 30px；0px 133px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|阅读正文容器 / reader / `.reader`|M|358.00×502.69|15px / 400 / 28.5px|12px 0px 30px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|阅读段落 / reader / `.reader p`|D|680.00×60.78|16px / 400 / 30.4px|0px；12px 0px；normal|0px / 0px none rgb(75, 88, 79)|rgb(75, 88, 79) / rgba(0, 0, 0, 0)|
|阅读段落 / reader / `.reader p`|M|358.00×85.50|15px / 400 / 28.5px|0px；12px 0px；normal|0px / 0px none rgb(75, 88, 79)|rgb(75, 88, 79) / rgba(0, 0, 0, 0)|
|偏好行 / settings / `.setting-row`|D|1098.00×95.53|14px / 400 / 23.1px|23px 0px；0px；20px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|偏好行 / settings / `.setting-row`|M|324.00×145.89|14px / 400 / 23.1px|23px 0px；0px；12px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|快捷宫格 / quick / `.quick-grid`|D|946.00×468.00|15px / 400 / 24.75px|0px；0px；12px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|快捷宫格 / quick / `.quick-grid`|M|358.00×620.00|15px / 400 / 24.75px|0px；0px；10px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|快捷卡 / quick / `.quick-card`|D|307.33×108.00|14px / 500 / 20.3px|18px；0px；10px|9px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|快捷卡 / quick / `.quick-card`|M|174.00×95.00|14px / 500 / 20.3px|16px；0px；10px|9px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|议事主区 / chat / `#work-main`|D|1224.00×824.00|15px / 400 / 24.75px|16px 24px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事主区 / chat / `#work-main`|M|390.00×718.00|15px / 400 / 24.75px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事容器 / chat / `.page-surface`|D|1176.00×792.00|15px / 400 / 24.75px|0px；0px；normal|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|议事容器 / chat / `.page-surface`|M|390.00×718.00|15px / 400 / 24.75px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|议事页体 / chat / `#page-body`|D|1174.00×690.50|15px / 400 / 24.75px|14px 20px 0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事页体 / chat / `#page-body`|M|390.00×622.50|15px / 400 / 24.75px|12px 16px 0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事对象行 / chat / `.chat-sessions`|D|1134.00×40.00|15px / 400 / 24.75px|0px 0px 4px；0px 0px 8px；8px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事对象行 / chat / `.chat-sessions`|M|358.00×40.00|15px / 400 / 24.75px|0px 0px 4px；0px 0px 8px；8px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事对象按钮 / chat / `.chat-sessions button`|D|78.00×36.00|13px / 500 / 18.85px|7px 12px；0px；7px|7px / 1px solid rgb(188, 205, 180)|rgb(33, 96, 77) / rgb(234, 240, 230)|
|议事对象按钮 / chat / `.chat-sessions button`|M|78.00×36.00|13px / 500 / 18.85px|7px 12px；0px；7px|7px / 1px solid rgb(188, 205, 180)|rgb(33, 96, 77) / rgb(234, 240, 230)|
|议事工具条 / chat / `.chat-toolbar`|D|1134.00×53.00|15px / 400 / 24.75px|0px 0px 10px；0px；8px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事工具条 / chat / `.chat-toolbar`|M|358.00×51.00|15px / 400 / 24.75px|0px 0px 10px；0px；8px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事工具条标题 / chat / `.chat-toolbar h3`|D|64.00×24.00|16px / 600 / 24px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事工具条标题 / chat / `.chat-toolbar h3`|M|64.00×24.00|16px / 600 / 24px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事滚动区 / chat / `#chat-stream`|D|1134.00×575.50|15px / 400 / 24.75px|16px 0px；0px；18px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事滚动区 / chat / `#chat-stream`|M|358.00×511.50|15px / 400 / 24.75px|16px 0px；0px；18px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事页脚 / chat / `#page-footer`|D|1174.00×99.50|15px / 400 / 24.75px|12px 20px；0px；16px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事页脚 / chat / `#page-footer`|M|390.00×95.50|15px / 400 / 24.75px|10px 16px；0px；16px|0px / |rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事输入排版 / chat / `.chat-composer`|D|1134.00×74.50|15px / 400 / 24.75px|0px；0px；6px 10px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事输入排版 / chat / `.chat-composer`|M|358.00×74.50|15px / 400 / 24.75px|0px；0px；6px 10px|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|议事输入框 / chat / `#chat-input`|D|1035.00×52.00|15px / 400 / 24px|12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|议事输入框 / chat / `#chat-input`|M|265.00×52.00|16px / 400 / 25.6px|12px；0px；normal|6px / 1px solid rgb(204, 210, 197)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|议事发送 / chat / `.chat-composer button`|D|89.00×48.00|14px / 500 / 20.3px|10px 16px；0px；7px|7px / 1px solid rgb(146, 63, 48)|rgb(255, 254, 250) / rgb(146, 63, 48)|
|议事发送 / chat / `.chat-composer button`|M|83.00×48.00|14px / 500 / 20.3px|10px 13px；0px；7px|7px / 1px solid rgb(146, 63, 48)|rgb(255, 254, 250) / rgb(146, 63, 48)|
|议事字数说明 / chat / `#chat-counter`|D|1134.00×16.50|11px / 400 / 16.5px|0px；0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|议事字数说明 / chat / `#chat-counter`|M|358.00×16.50|11px / 400 / 16.5px|0px；0px；normal|0px / 0px none rgb(104, 113, 107)|rgb(104, 113, 107) / rgba(0, 0, 0, 0)|
|消息头像 / chat-populated / `.chat-message .portrait`|D|32.00×32.00|15px / 400 / 24.75px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|消息头像 / chat-populated / `.chat-message .portrait`|M|28.00×28.00|15px / 400 / 24.75px|0px；0px；normal|50% / 1px solid rgb(216, 216, 201)|rgb(36, 46, 43) / rgb(238, 234, 222)|
|消息气泡 / chat-populated / `.chat-bubble`|D|150.00×51.50|15px / 400 / 25.5px|12px 14px；0px；normal|8px 0px 8px 8px / 1px solid rgb(219, 228, 211)|rgb(36, 46, 43) / rgb(234, 240, 230)|
|消息气泡 / chat-populated / `.chat-bubble`|M|138.00×45.80|14px / 400 / 23.8px|10px 12px；0px；normal|8px 0px 8px 8px / 1px solid rgb(219, 228, 211)|rgb(36, 46, 43) / rgb(234, 240, 230)|
|本人气泡 / chat-populated / `.me .chat-bubble`|D|150.00×51.50|15px / 400 / 25.5px|12px 14px；0px；normal|8px 0px 8px 8px / 1px solid rgb(219, 228, 211)|rgb(36, 46, 43) / rgb(234, 240, 230)|
|本人气泡 / chat-populated / `.me .chat-bubble`|M|138.00×45.80|14px / 400 / 23.8px|10px 12px；0px；normal|8px 0px 8px 8px / 1px solid rgb(219, 228, 211)|rgb(36, 46, 43) / rgb(234, 240, 230)|
|弹层议事 / chat-dialog / `#panel`|D|1000.00×780.00|15px / 400 / 24.75px|0px；0px；normal|12px / 1px solid rgb(227, 229, 220)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|弹层议事 / chat-dialog / `#panel`|M|390.00×844.00|15px / 400 / 24.75px|0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgb(255, 254, 250)|
|弹层议事页体 / chat-dialog / `#panel-body`|D|998.00×613.50|15px / 400 / 24.75px|16px 20px 0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|弹层议事页体 / chat-dialog / `#panel-body`|M|390.00×674.50|15px / 400 / 24.75px|12px 16px 0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|弹层议事页脚 / chat-dialog / `#panel-footer`|D|998.00×99.50|15px / 400 / 24.75px|12px 20px；0px；12px|0px / |rgb(36, 46, 43) / rgb(245, 244, 240)|
|弹层议事页脚 / chat-dialog / `#panel-footer`|M|390.00×95.50|15px / 400 / 24.75px|10px 16px；0px；8px|0px / |rgb(36, 46, 43) / rgb(245, 244, 240)|
|登录表单 / login / `.login-form`|D|390.00×506.59|15px / 400 / 24.75px|0px；0px 138px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|登录表单 / login / `.login-form`|M|358.00×512.59|15px / 400 / 24.75px|8px 0px 0px；0px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|新手标题 / guide-0 / `.brand-text`|D|666.00×39.00|26px / 500 / 39px|0px；10px 0px 18px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|新手标题 / guide-0 / `.brand-text`|M|358.00×39.00|26px / 500 / 39px|0px；10px 0px 18px；normal|0px / 0px none rgb(36, 46, 43)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|地图工具条 / map / `.map-hud`|D|342.00×52.00|15px / 400 / 24.75px|6px 8px；0px；5px|10px / 1px solid rgba(165, 135, 83, 0.36)|rgb(240, 223, 189) / rgba(39, 31, 23, 0.92)|
|地图工具条 / map / `.map-hud`|M|370.00×52.00|15px / 400 / 24.75px|6px；0px；3px|10px / 1px solid rgba(165, 135, 83, 0.36)|rgb(240, 223, 189) / rgba(39, 31, 23, 0.92)|
|地图场所按钮 / map / `.landmark`|D|98.18×40.91|15px / 500 / 21px|8px 12px；0px；7px|5px / 1px solid rgba(179, 148, 92, 0.61)|rgb(242, 223, 181) / rgba(44, 33, 26, 0.918)|
|地图场所按钮 / map / `.landmark`|M|89.20×38.36|14px / 500 / 19.6px|8px 12px；0px；7px|5px / 1px solid rgba(179, 148, 92, 0.61)|rgb(242, 223, 181) / rgba(44, 33, 26, 0.918)|
|地图好汉热区 / map / `.agent-hit`|D|53.18×65.45|14px / 500 / 20.3px|0px；0px；7px|50% / 2px solid rgba(0, 0, 0, 0)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
|地图好汉热区 / map / `.agent-hit`|M|49.87×61.38|14px / 500 / 20.3px|0px；0px；7px|50% / 2px solid rgba(0, 0, 0, 0)|rgb(36, 46, 43) / rgba(0, 0, 0, 0)|
