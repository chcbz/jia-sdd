window.CHANGE_ANNOTATIONS = [
  {
    "id": "request",
    "title": "提需求 · 办事首页",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-request.png",
    "boxes": [
      {
        "selector": ".quick-request-actions",
        "title": "入口合并",
        "note": "取消独立“参考图”，统一为“添加资料（可选）”；不加资料也能开始。",
        "x": 371,
        "y": 487.5625,
        "w": 989,
        "h": 43.09375
      },
      {
        "selector": ".overview-quick-request .mmd-attachments",
        "title": "资料随需求带入",
        "note": "已选资料统一展示，可预览、移除，不区分专门的参考图入口。",
        "x": 371,
        "y": 540.65625,
        "w": 989,
        "h": 94.78125
      }
    ]
  },
  {
    "id": "create",
    "title": "提需求 · 张榜表单",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-create.png",
    "boxes": [
      {
        "selector": ".task-create-form .mmd",
        "title": "同样统一资料",
        "note": "现有张榜表单也使用同一资料选择方式，不再出现专门的参考图片面板。",
        "x": 614.375,
        "y": 259,
        "w": 489.125,
        "h": 186
      }
    ]
  },
  {
    "id": "materials",
    "title": "选择资料",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-materials.png",
    "boxes": [
      {
        "selector": ".mmd-files",
        "title": "不只选图片",
        "note": "从工作空间选择图片、文档、音频或文本；参考图只是图片在任务中的用途。",
        "x": 416,
        "y": 337.140625,
        "w": 608,
        "h": 348.90625
      },
      {
        "selector": "dialog footer",
        "title": "选择可取消",
        "note": "确认才更新已选资料；取消保留原选择，没有资料也能继续。",
        "x": 416,
        "y": 702.046875,
        "w": 608,
        "h": 38.390625
      }
    ]
  },
  {
    "id": "agents",
    "title": "点将册",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-agents.png",
    "boxes": [
      {
        "selector": ".mmd-agent-detail",
        "title": "点将后直接议事",
        "note": "保留原名册选人方式；点击“点将并议事”后自动带上当前需求和资料，无需再手动发送。",
        "x": 907,
        "y": 239,
        "w": 320,
        "h": 638
      }
    ]
  },
  {
    "id": "chat-start",
    "title": "悬赏议事 · 自动带入需求",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-chat-start.png",
    "boxes": [
      {
        "selector": ".hall-message.USER",
        "title": "自动首条消息",
        "note": "这里的需求与资料由点将自动带入。Agent 可以直接执行，也可以在会话中自然澄清。",
        "x": 314.96875,
        "y": 321.9375,
        "w": 889.03125,
        "h": 205.265625
      },
      {
        "selector": ".composer-body",
        "title": "只用普通发送",
        "note": "取消“生成图片”“受控请求”及重复批准，不需要选择工具或办理模式。",
        "x": 221,
        "y": 807.859375,
        "w": 998,
        "h": 44
      }
    ]
  },
  {
    "id": "chat-result",
    "title": "悬赏议事 · 图片与继续修改",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-chat-result.png",
    "boxes": [
      {
        "selector": ".mmd-result img",
        "title": "在消息中看成果",
        "note": "统一在会话内显示图片，点击放大；不另开一套绘图流程。",
        "x": 246,
        "y": 401.078125,
        "w": 350,
        "h": 223.609375
      },
      {
        "selector": ".mmd-result .mmd-row",
        "title": "预览、下载、保存、引用",
        "note": "保存到工作空间是可选操作；引用当前稿继续改，旧稿仍保留。",
        "x": 246,
        "y": 632.6875,
        "w": 839.03125,
        "h": 38.390625
      },
      {
        "selector": ".mmd-composer-extra",
        "title": "继续补充资料",
        "note": "不重提需求、不重新点将，可直接在当前会话补充图片、文档或音频。",
        "x": 221,
        "y": 763.671875,
        "w": 998,
        "h": 37.1875
      },
      {
        "selector": ".toolbar-actions [data-action=accept]",
        "title": "验收同一事项",
        "note": "会话内直达同一个验收入口，与事项详情中的入口一致。",
        "x": 1175,
        "y": 257.546875,
        "w": 52,
        "h": 38.390625
      }
    ]
  },
  {
    "id": "chat-media",
    "title": "悬赏议事 · 音频与文档",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-chat-media.png",
    "boxes": [
      {
        "selector": ".mmd-result audio",
        "title": "音频原位播放",
        "note": "语音、音频类成果可直接播放，也可下载或保存。这里使用示意音。",
        "x": 246,
        "y": 362.078125,
        "w": 350,
        "h": 54
      },
      {
        "selector": ".mmd-result[data-result=result-3]",
        "title": "文档也是成果",
        "note": "文档与文字和图片一样，可在会话中预览、下载并用于验收。",
        "x": 233,
        "y": 519.859375,
        "w": 865.03125,
        "h": 199.8125
      }
    ]
  },
  {
    "id": "workspace",
    "title": "资料 · 现有工作空间",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-workspace.png",
    "boxes": [
      {
        "selector": ".treasure-file-row:last-child",
        "title": "保存后在这里找到",
        "note": "继续使用现有工作空间，不新增一套文件系统；保存的成果可以再次作为资料使用。",
        "x": 271,
        "y": 733.796875,
        "w": 1114,
        "h": 101.78125
      }
    ]
  },
  {
    "id": "detail",
    "title": "事项详情",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-detail.png",
    "boxes": [
      {
        "selector": ".matter-advice-card",
        "title": "进展与继续议事",
        "note": "去掉“明确开始正式办理”等重复执行说明，保留进展和继续议事动作。",
        "x": 257,
        "y": 166,
        "w": 1142,
        "h": 234.671875
      },
      {
        "selector": ".task-material-links",
        "title": "需求资料与成果",
        "note": "在同一事项查看关联资料和成果数量；不再限定为正式 PDF 办理。",
        "x": 257,
        "y": 414.671875,
        "w": 1142,
        "h": 221.578125
      },
      {
        "selector": ".matter-results-action",
        "title": "保留原验收入口",
        "note": "从这里查看成果并选择最终交付，与会话中的验收是同一流程。",
        "x": 257,
        "y": 650.25,
        "w": 1142,
        "h": 44
      }
    ]
  },
  {
    "id": "accept",
    "title": "验收成果",
    "device": "desktop",
    "width": 1440,
    "height": 1000,
    "image": "screenshots/desktop-accept.png",
    "boxes": [
      {
        "selector": ".mmd-selection",
        "title": "选择具体稿次",
        "note": "图片、音频、文档和文字都可选；可以只验收文字，也可以组合多项成果。",
        "x": 416,
        "y": 367.625,
        "w": 608,
        "h": 295.125
      },
      {
        "selector": "dialog footer",
        "title": "满意后完成",
        "note": "可回到议事继续修改；确认验收后事项完成，无需先保存到工作空间。",
        "x": 416,
        "y": 678.75,
        "w": 608,
        "h": 38.390625
      }
    ]
  },
  {
    "id": "request",
    "title": "提需求 · 办事首页",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-request.png",
    "boxes": [
      {
        "selector": ".quick-request-actions",
        "title": "入口合并",
        "note": "取消独立“参考图”，统一为“添加资料（可选）”；不加资料也能开始。",
        "x": 35,
        "y": 402.5625,
        "w": 320,
        "h": 43.09375
      },
      {
        "selector": ".overview-quick-request .mmd-attachments",
        "title": "资料随需求带入",
        "note": "已选资料统一展示，可预览、移除，不区分专门的参考图入口。",
        "x": 35,
        "y": 455.65625,
        "w": 320,
        "h": 94.78125
      }
    ]
  },
  {
    "id": "create",
    "title": "提需求 · 张榜表单",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-create.png",
    "boxes": [
      {
        "selector": ".task-create-form .mmd",
        "title": "同样统一资料",
        "note": "现有张榜表单也使用同一资料选择方式，不再出现专门的参考图片面板。",
        "x": 16,
        "y": 314,
        "w": 358,
        "h": 186
      }
    ]
  },
  {
    "id": "materials",
    "title": "选择资料",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-materials.png",
    "boxes": [
      {
        "selector": ".mmd-files",
        "title": "不只选图片",
        "note": "从工作空间选择图片、文档、音频或文本；参考图只是图片在任务中的用途。",
        "x": 32,
        "y": 259.140625,
        "w": 326,
        "h": 348.90625
      },
      {
        "selector": "dialog footer",
        "title": "选择可取消",
        "note": "确认才更新已选资料；取消保留原选择，没有资料也能继续。",
        "x": 32,
        "y": 624.046875,
        "w": 326,
        "h": 38.390625
      }
    ]
  },
  {
    "id": "agents",
    "title": "点将册",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-agents.png",
    "boxes": [
      {
        "selector": ".mmd-agent-detail",
        "title": "点将后直接议事",
        "note": "保留原名册选人方式；点击“点将并议事”后自动带上当前需求和资料，无需再手动发送。",
        "x": 37,
        "y": 625.796875,
        "w": 316,
        "h": 185.203125
      }
    ]
  },
  {
    "id": "chat-start",
    "title": "悬赏议事 · 自动带入需求",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-chat-start.png",
    "boxes": [
      {
        "selector": ".hall-message.USER",
        "title": "自动首条消息",
        "note": "这里的需求与资料由点将自动带入。Agent 可以直接执行，也可以在会话中自然澄清。",
        "x": 41,
        "y": 263.03125,
        "w": 308,
        "h": 205.265625
      },
      {
        "selector": ".composer-body",
        "title": "只用普通发送",
        "note": "取消“生成图片”“受控请求”及重复批准，不需要选择工具或办理模式。",
        "x": 37,
        "y": 732.859375,
        "w": 316,
        "h": 44
      }
    ]
  },
  {
    "id": "chat-result",
    "title": "悬赏议事 · 图片与继续修改",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-chat-result.png",
    "boxes": [
      {
        "selector": ".mmd-result img",
        "title": "在消息中看成果",
        "note": "统一在会话内显示图片，点击放大；不另开一套绘图流程。",
        "x": 64,
        "y": 324.171875,
        "w": 262,
        "h": 167.375
      },
      {
        "selector": ".mmd-result .mmd-row",
        "title": "预览、下载、保存、引用",
        "note": "保存到工作空间是可选操作；引用当前稿继续改，旧稿仍保留。",
        "x": 64,
        "y": 499.546875,
        "w": 262,
        "h": 84.78125
      },
      {
        "selector": ".mmd-composer-extra",
        "title": "继续补充资料",
        "note": "不重提需求、不重新点将，可直接在当前会话补充图片、文档或音频。",
        "x": 37,
        "y": 689.671875,
        "w": 316,
        "h": 37.1875
      },
      {
        "selector": ".toolbar-actions [data-action=accept]",
        "title": "验收同一事项",
        "note": "会话内直达同一个验收入口，与事项详情中的入口一致。",
        "x": 199,
        "y": 202.640625,
        "w": 52,
        "h": 38.390625
      }
    ]
  },
  {
    "id": "chat-media",
    "title": "悬赏议事 · 音频与文档",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-chat-media.png",
    "boxes": [
      {
        "selector": ".mmd-result audio",
        "title": "音频原位播放",
        "note": "语音、音频类成果可直接播放，也可下载或保存。这里使用示意音。",
        "x": 64,
        "y": 307.171875,
        "w": 262,
        "h": 54
      },
      {
        "selector": ".mmd-result[data-result=result-3]",
        "title": "文档也是成果",
        "note": "文档与文字和图片一样，可在会话中预览、下载并用于验收。",
        "x": 53,
        "y": 509.34375,
        "w": 284,
        "h": 115.53125
      }
    ]
  },
  {
    "id": "workspace",
    "title": "资料 · 现有工作空间",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-workspace.png",
    "boxes": [
      {
        "selector": ".treasure-file-row:last-child",
        "title": "保存后在这里找到",
        "note": "继续使用现有工作空间，不新增一套文件系统；保存的成果可以再次作为资料使用。",
        "x": 16,
        "y": 618.84375,
        "w": 358,
        "h": 93.78125
      }
    ]
  },
  {
    "id": "detail",
    "title": "事项详情",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-detail.png",
    "boxes": [
      {
        "selector": ".matter-advice-card",
        "title": "进展与继续议事",
        "note": "去掉“明确开始正式办理”等重复执行说明，保留进展和继续议事动作。",
        "x": 12,
        "y": 69,
        "w": 366,
        "h": 234.671875
      },
      {
        "selector": ".task-material-links",
        "title": "需求资料与成果",
        "note": "在同一事项查看关联资料和成果数量；不再限定为正式 PDF 办理。",
        "x": 12,
        "y": 317.671875,
        "w": 366,
        "h": 217.578125
      },
      {
        "selector": ".matter-results-action",
        "title": "保留原验收入口",
        "note": "从这里查看成果并选择最终交付，与会话中的验收是同一流程。",
        "x": 12,
        "y": 549.25,
        "w": 366,
        "h": 44
      }
    ]
  },
  {
    "id": "accept",
    "title": "验收成果",
    "device": "mobile",
    "width": 390,
    "height": 844,
    "image": "screenshots/mobile-accept.png",
    "boxes": [
      {
        "selector": ".mmd-selection",
        "title": "选择具体稿次",
        "note": "图片、音频、文档和文字都可选；可以只验收文字，也可以组合多项成果。",
        "x": 32,
        "y": 300.828125,
        "w": 326,
        "h": 295.125
      },
      {
        "selector": "dialog footer",
        "title": "满意后完成",
        "note": "可回到议事继续修改；确认验收后事项完成，无需先保存到工作空间。",
        "x": 32,
        "y": 611.953125,
        "w": 326,
        "h": 38.390625
      }
    ]
  }
];
