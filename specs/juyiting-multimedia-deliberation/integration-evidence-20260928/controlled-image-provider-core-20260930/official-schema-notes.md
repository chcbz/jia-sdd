# 受控图像HTTP adapter：官方契约来源

本包只核验公开schema，不调用Provider、不选择模型/账户，不证明实际账户权限或账单金额。

- 官方edit方法参考确认JSON `images`数组及base64 data URL；最大16张，image_url长度上限20971520。明确n=1和PNG输出，返回b64_json。
- 官方generate方法参考确认prompt/model/n/output_format；GPT image不使用response_format，PNG结果从b64_json读取。
- 方法URL与定位范围见本目录JSON。宿主直接抓取曾403；后来官方web返回的方法正文建立了文档证据，旧失败未改写。实际Provider兼容性仍NOT_RUN。

不保存/复刻全文；仅记录本adapter所需字段。冻结core仍不接原grant/START费用桥，不替代多轮/双接应/34产品验收与版本发布。
