# good-habits-skill

> 一个为 AI Agent（Claude / Claude Code 等）注入「好习惯」的可加载 Skill。让 Agent 在开发场景中自然遵循规范工作流，并通过本地 Q&A 档案缓解**每开一个新对话就丢失上下文**的窘况。

---

## 为什么需要这个 Skill？

LLM Agent 的会话级上下文是**易失**的：

- 关掉 IDE 重开 → 上下文没了。
- 切到新对话 → 上下文没了。
- 用户被迫每次重新交代："我们之前是这样定的……" "上次踩过 XXX 坑……"

这不只是体验问题，更直接影响产出质量——Agent 看不到历史决策，就会重复造轮子、推翻已经定过的方案、踩同样的坑。

**本 Skill 的解决思路是让 Agent 自己写工作日志，下次新会话自己回看。** 整个机制纯本地、零外部依赖，工作日志就是项目里的几个 Markdown 文件，人和 Agent 都能直接读、直接编辑、随仓库一起走。

---

## 六大习惯一览

| # | 习惯名 | 触发时机 | 一句话描述 |
| - | --- | --- | --- |
| 1 | 先出方案再动手 | 用户要改代码 / 给了 PRD | 先出 Markdown 实施方案让用户 Review，**等明确通过**再动手 |
| 2 | 多方案对比 | 某功能点存在多种实现 | 用表格列出所有方案的优劣，让用户拍板 |
| 3 | 自动记录 Q&A | 每次代码改动完成后 | 在 `.good-habits/YYYY-MM-DD-HH-mm-ss.md` 落盘 Q&A |
| 4 | 二方包发布顺序提示 | 涉及二方包 / SDK / starter 版本联动 | 用表格说清依赖关系 + Maven 标准引用片段 |
| 5 | 新对话启动时回顾历史 | 新会话第一次涉及本项目的实质请求 | 主动扫 `.good-habits/` 最近若干条记录，恢复上下文再回答 |
| 6 | Java 注释规范 | 新建 Java 类/枚举/接口/方法/静态变量/实例变量 | 按 `@author 鹤童 / @desc / @date` 等固定格式补全 Javadoc |

> **习惯三 + 习惯五 是一对**：写入侧负责沉淀知识，读取侧负责跨会话恢复——这是本 Skill 缓解"开新对话即失忆"问题的核心机制。

---

## 目录结构

```
good-habits-skill/
├── SKILL.md                          # Skill 主入口（含 YAML frontmatter + 五大习惯的触发条件与行为规范）
├── README.md                         # 你正在看的这份文档
├── scripts/
│   ├── create-qa-record.sh           # 习惯三：Bash 版自动建档脚本
│   └── create-qa-record.py           # 习惯三：Python 版自动建档脚本（无 Bash 环境时使用）
├── references/
│   ├── plan-template.md              # 习惯一：实施方案模板
│   ├── comparison-template.md        # 习惯二：多方案对比模板
│   ├── maven-release-order.md        # 习惯四：二方包发布顺序详细参考
│   └── java-comment-standard.md      # 习惯六：Java 注释格式样例与自查清单
└── assets/
    └── qa-template.md                # 习惯三：Q&A 记录的 Markdown 模板
```

---

## 怎么用

### 1. 把 Skill 加载到你的 Agent

将本目录放到 Agent 可发现 Skill 的位置（具体路径取决于宿主，例如 Claude Code 的 `~/.claude/skills/` 或项目级 `.claude/skills/`）。Agent 在启动时会读取 `SKILL.md` 的 frontmatter，根据 `description` 决定何时调用。

### 2. 正常和 Agent 协作

加载完成后，**用户什么都不用做**——Agent 会在以下时机自动行动：

- 你提需求 → Agent 先给方案让你 Review（习惯一）。
- 多种实现 → Agent 列表格让你选（习惯二）。
- 改完代码 → Agent 自动写 Q&A 落盘（习惯三）。
- 问二方包 → Agent 给依赖表 + Maven 片段（习惯四）。
- 你开新对话进入项目 → Agent 先回看 `.good-habits/` 再答（习惯五）。
- 写 Java 代码 → Agent 自动按规范格式落 Javadoc 与注释（习惯六）。

### 3. 项目里多了 `.good-habits/`，怎么办？

第一次触发习惯三时，Agent 会在你的项目根目录创建 `.good-habits/`。**是否纳入版本管理由你决定**：

- **纳入仓库**：团队成员（包括他们的 Agent）共享同一份项目记忆，适合多人协作项目。
- **加 `.gitignore`**：仅个人本地使用，避免污染历史。

Agent 不会替你做这个决定，第一次创建时会主动询问一次。

### 4. 手动调用脚本（可选）

`scripts/create-qa-record.sh` 也支持手工调用：

```bash
./scripts/create-qa-record.sh /path/to/your/project \
  "增加登录功能" \
  "JWT + Redis 缓存" \
  "src/auth.ts: 新增登录接口" \
  "需要在生产环境配置 JWT_SECRET"
```

会在 `/path/to/your/project/.good-habits/` 下生成一个时间戳命名的 Markdown 文件，并把绝对路径打印到 stdout。Python 版同理：

```bash
python3 scripts/create-qa-record.py /path/to/your/project \
  --question "增加登录功能" \
  --solution "JWT + Redis 缓存" \
  --files "src/auth.ts: 新增登录接口" \
  --notes "需要在生产环境配置 JWT_SECRET"
```

---

## Q&A 记录文件长什么样

每次代码改动后，`.good-habits/` 下会多一个文件，例如 `2026-05-14-15-32-08.md`：

```markdown
# Q&A 记录 - 2026-05-14-15-32-08

> 由 good-habits-skill 自动生成

## 用户问题
增加登录功能，要求支持账号密码 + 短信验证码两种方式。

## 实现方案
基于 JWT 的鉴权 + Redis 短信码缓存。前端拆为 LoginForm / SmsLoginForm 两个组件。

## 修改的文件及内容摘要
- src/auth/jwt.ts: 新增 issueToken / verifyToken
- src/auth/sms.ts: 新增短信验证码发送与校验
- src/pages/Login.tsx: 拆分为两种登录方式

## 备注
- 需在生产环境配置 JWT_SECRET 与短信网关的 AK/SK。
- 短信码 TTL 暂定 5 分钟，待运营反馈后调整。
```

下一次新对话时，Agent 会自动看到这些信息，无需你重复交代。

---

## 与平台级 Memory 的关系

如果你的 Agent 客户端（如 Claude Code）已经启用了平台级 memory 功能，本 Skill 与之**并行不悖**：

| 维度 | 平台 Memory | `.good-habits/`（本 Skill） |
| --- | --- | --- |
| 颗粒度 | 跨项目，关于"用户" | 单项目，关于"工作流水" |
| 存储位置 | 平台账户下 | 项目仓库内 |
| 可见性 | 仅本人 | 团队（若纳入版本管理） |
| 内容性质 | 用户画像 / 偏好 / 长期共识 | 需求 / 决策 / 改动 / 踩坑 |
| 是否随项目走 | 否 | 是 |

简单说：**Memory 记住"你是谁、你怎么工作"；`.good-habits/` 记住"这个项目发生过什么"。**

---

## FAQ

**Q：Agent 真的会自动遵守这些习惯吗？还是要我每次提醒？**
A：Skill 加载后，Agent 应当主动判断触发条件并执行。如果发现 Agent 没遵守，最常见的原因是 Skill 没被正确加载，或者宿主环境对 Skill 的支持有限——可以试着在对话开头显式说"请遵循 good-habits-skill"。

**Q：`.good-habits/` 越积越多怎么办？**
A：保持原样即可。Agent 默认只读最近 3~5 条；老记录作为"项目档案"留底，人也能随时翻阅。如果觉得太大，定期归档到子目录（如 `.good-habits/2025/`）即可，不影响 Skill 工作。

**Q：能否关掉某个习惯？**
A：可以。直接在 `SKILL.md` 中删掉对应章节，或者在使用时明确告诉 Agent："这次跳过习惯一直接动手"。

**Q：习惯五会不会拖慢响应？每次新对话都要先读一堆文件。**
A：只在**新对话的第一次实质请求**触发一次，且只读最近 3~5 条。代价远小于"用户重新交代背景"的成本。

---

## 版本

- **v1.2.0**（2026-05-18）：新增习惯六（Java 注释规范），覆盖类/枚举/接口/方法/静态变量/实例变量/方法内变量七类元素的注释格式约束。
- **v1.1.0**（2026-05-14）：新增习惯五（会话启动回顾），明确"项目记忆层"定位。
- **v1.0.0**：初版，含习惯一~四。

## License

MIT
