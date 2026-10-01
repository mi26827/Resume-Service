# backend-repo-career-miner

[English](README.md)

`Resume-Service` 是这个 Git 仓库的名称；其中的 Codex Skill 名为 `backend-repo-career-miner`。虽然仓库名里有 Service，本项目**不是**在线简历网站、简历托管服务或后端服务，而是一套提示词、参考资料和脚本，用于让 Codex 分析经授权的本地代码仓库，并生成有证据支持的职业材料。

## 适用人群

适合希望理解后端代码库、复核自己有 Git 证据支持的工作、准备技术面试，或根据可核查的工程证据整理简历的学生、求职者和软件工程师。Skill 不依赖特定语言或框架，包含 Java/Kotlin、Go、Python、Node.js、Rust、C#、Ruby 和 PHP 的技术栈识别指南。

分析输入是本地仓库路径。`DISCOVERY` 不需要候选人身份。若要分析个人贡献，必须由用户提供并确认能够识别其提交的 Git 作者姓名和/或邮箱。没有用户确认的身份信息时，Skill 不得猜测哪些提交属于用户；仍可描述项目具备的能力，但不能将其归属到个人。

## 安装与更新

安装目录必须使用 Skill 名称 `backend-repo-career-miner`，即使源仓库名为 `Resume-Service` 也是如此。若设置了 `CODEX_HOME`，安装位置为 `$CODEX_HOME/skills/backend-repo-career-miner`；若未设置，默认位置为 `$HOME/.codex/skills/backend-repo-career-miner`。

### 首次安装

直接克隆到最终 Skill 目录。以下命令发现目标目录已存在时会提示检查，不会覆盖目录内容，也不会额外嵌套创建 `Resume-Service` 目录。

#### macOS / Linux（shell）

```bash
skills_root="${CODEX_HOME:-$HOME/.codex}/skills"
target="$skills_root/backend-repo-career-miner"
if [ -e "$target" ]; then
  printf 'Install directory already exists; inspect it before proceeding: %s\n' "$target" >&2
else
  mkdir -p "$skills_root"
  git clone https://github.com/mi26827/Resume-Service.git "$target"
fi
```

#### Windows（PowerShell）

```powershell
if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
    $skillsRoot = Join-Path $HOME ".codex\skills"
} else {
    $skillsRoot = Join-Path $env:CODEX_HOME "skills"
}
$target = Join-Path $skillsRoot "backend-repo-career-miner"
if (Test-Path -LiteralPath $target) {
    throw "Install directory already exists; inspect it before proceeding: $target"
}
if (-not (Test-Path -LiteralPath $skillsRoot)) {
    New-Item -ItemType Directory -Path $skillsRoot | Out-Null
}
git clone https://github.com/mi26827/Resume-Service.git "$target"
if ($LASTEXITCODE -ne 0) { throw "git clone failed; inspect the target before retrying." }
```

安装后如果 Codex 尚未识别该 Skill，请重新加载或重启 Codex。

### 更新已有 Git 克隆

先检查安装目录；仅当工作区干净时才执行更新。`--ff-only` 不会创建合并提交，并会在本地分支与远程分叉时拒绝更新。

#### macOS / Linux（shell）

```bash
target="${CODEX_HOME:-$HOME/.codex}/skills/backend-repo-career-miner"
git -C "$target" status --short --branch
git -C "$target" diff
```

确认 Git 工作区干净后再更新：

```bash
target="${CODEX_HOME:-$HOME/.codex}/skills/backend-repo-career-miner"
git -C "$target" pull --ff-only
```

#### Windows（PowerShell）

```powershell
if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
    $skillsRoot = Join-Path $HOME ".codex\skills"
} else {
    $skillsRoot = Join-Path $env:CODEX_HOME "skills"
}
$target = Join-Path $skillsRoot "backend-repo-career-miner"
git -C "$target" status --short --branch
git -C "$target" diff
```

确认 Git 工作区干净后再更新：

```powershell
if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
    $skillsRoot = Join-Path $HOME ".codex\skills"
} else {
    $skillsRoot = Join-Path $env:CODEX_HOME "skills"
}
$target = Join-Path $skillsRoot "backend-repo-career-miner"
git -C "$target" pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Update stopped; inspect the local and remote histories before proceeding." }
```

如果目标目录已存在，安装或更新前先检查目录状态。如果 `git status` 显示本地改动，先审阅改动，并将整个目录（包括隐藏文件和未跟踪文件）复制到一个确认尚不存在的新位置作为恢复副本；保存或合并这些改动后再更新。不要使用强制拉取、reset、clean 或直接覆盖目录。如果 `git status` 表明它不是 Git 克隆（例如从压缩包复制而来），请把新版本克隆到另一个确认未占用的暂存目录，与现有安装进行比较。先备份现有目录，再手动迁移本地改动；确认目标为空后才切换活动目录。在 Codex 识别更新后的 Skill 前保留备份。不要直接克隆或复制到已有安装目录上。

## 快速开始：生成第一份 DISCOVERY 报告

选择一个你有权检查的本地后端仓库，在 Codex 中提出：

```text
Use $backend-repo-career-miner to analyze this repository:
<本地后端仓库的绝对路径>

Mode: DISCOVERY
```

默认情况下，报告写入目标仓库内的 `career-miner-output/`。DISCOVERY 会生成 `SUMMARY.md`、`01-project-overview.md`、`02-tech-stack.md` 和 `03-architecture-analysis.md`。运行结束后即可在本地查看这些文件。

参见 [`examples/tiny-task-api/README.md`](examples/tiny-task-api/README.md)，其中包含可快速试跑的教学样例及对应报告。所有内容均为合成内容，不是真实生产案例。

## 选择分析模式

每次运行都会生成 `SUMMARY.md`。标准模式恰好生成以下编号报告：

| 模式 | 用途 | 编号报告 |
|---|---|---|
| `DISCOVERY` | 项目目的、实际使用的技术及架构 | `01`–`03` |
| `CONTRIBUTION` | 基于 Git 证据分析候选人贡献和后端工程能力 | `04`–`05` |
| `AI_AGENT` | 现有 AI 能力及 Agent 机会是否成立 | `07`–`08` |
| `RESUME` | 有证据支持的简历要点和面试准备 | `06`、`09` |
| `FULL` | 一次完成全部分析 | `01`–`09` |
| `CUSTOM` | 用户指定的报告子集 | 仅指定报告 |

默认模式是 `DISCOVERY`。`FULL` 会覆盖所有分析方向，必须由用户明确指定。窄模式可以在内部分析必要的前置内容，但不会悄悄在输出中增加无关报告。

其他模式的请求示例：

```text
Use $backend-repo-career-miner in AI_AGENT mode on <本地仓库路径>.
Check existing AI capabilities and whether a real Agent opportunity exists.
Do not force an Agent.
```

```text
Use $backend-repo-career-miner in RESUME mode on <本地仓库路径>.
Target role: Backend Engineer
Experience level: Intern
Resume language: Chinese
```

如需生成辅助学习的项目技术栈 PDF，可在 `DISCOVERY` 或 `FULL` 请求中明确提出。文档会解释各技术在项目中的职责、实现位置、组件协作和相关概念，并附代码引用；它不依赖个人贡献归属。导出需要环境可调用 Chromium，细节见 [`references/project-learning-pdf.md`](references/project-learning-pdf.md)。

```text
Use $backend-repo-career-miner to analyze this repository:
<本地仓库绝对路径>

Mode: DISCOVERY
准备生成中文项目技术栈学习 PDF。逐项解释技术在项目中的职责、实际使用方式、组件协作、关键概念，并附代码位置。先给我可编辑的 Markdown 草稿并等待我审阅；我确认后再生成 PDF。
```

```text
Use $backend-repo-career-miner in FULL mode on <本地仓库路径>.
```

只有最后一个请求会选择 `FULL`，Skill 不得自行推断用户想运行 FULL。使用 `CUSTOM` 时，应列出要生成的准确编号报告。

进行贡献分析时，请在请求中写明并确认 Git 身份，例如：

```text
Use $backend-repo-career-miner in CONTRIBUTION mode on <本地仓库路径>.

Candidate Git identity (confirmed by me):
<作者姓名> 和/或 <作者邮箱>
```

也可以提供候选时间范围。如果没有确认的身份信息，作者归属保持未知，不得声称个人贡献。源代码可以证明项目具备什么能力，不能证明是谁编写了它。

## 证据与隐私边界

Skill 从本地文件系统读取目标仓库，并将报告写入所选的本地输出目录。本仓库不包含源代码上传器或遥测。Codex 仍会按用户配置的运行环境和数据处理设置处理分析所需内容；分析受限仓库前，请确认这些设置允许此类分析。仅使用本 Skill 检查你有权访问的仓库，不要要求它发布私有代码。生成的报告不得复述密钥、凭据、内部域名或大段源代码。

输出会区分三类陈述：

- `PROJECT_CAPABILITY`：项目中实际存在的能力，并有实现证据支持。
- `PERSONAL_CONTRIBUTION`：只有独立的 Git 归属证据支持时，才归因给候选人。实现证据本身不等于作者身份。
- `EXPLORATION`：未来可能进行的调查或设计，不代表已经完成的项目工作。

每项主张分别记录两个证据维度：**Implementation Evidence（实现证据）**说明能力是否存在并接入运行路径；**Attribution Evidence（归属证据）**说明候选人是否实质参与。简历内容按证据漏斗生成：先理解项目，再确认候选人归属，提炼原子级工程发现并分组，最后撰写项目经历。没有依据时不编造性能或规模指标。Agent 方案不是必选结论，必须有证据支持的工作流、实际判断需求、工具使用、评估方式和安全边界；确定性自动化或没有合适机会也都是有效判断。目标岗位、经验级别和简历语言可以影响表达方式，但不能改变项目事实或证据等级。

## 输出契约与校验

契约 0.2 对各模式输出文件的定义见 [`references/output-contract.md`](references/output-contract.md)。在本仓库目录下校验生成结果：

```bash
OUTPUT_DIR="/绝对路径/career-miner-output"
python3 scripts/validate_output.py "$OUTPUT_DIR"
```

校验 `CUSTOM` 时，必须传入用户选择的准确报告文件名（不包含 `SUMMARY.md`）：

```bash
OUTPUT_DIR="/绝对路径/career-miner-output"
python3 scripts/validate_output.py "$OUTPUT_DIR" \
  --custom-reports 01-project-overview.md 03-architecture-analysis.md
```

校验器检查头部、报告集合一致性和部分结构要求。校验通过不代表陈述一定属实、Git 身份正确、引用有效或简历内容真实；这些仍需基于证据审阅。

## 可选项目技术学习 PDF

Skill 会先生成 `exports/project-learning-guide.md` 草稿并询问你是否符合学习需要；你可以直接编辑该文件或提出修改意见。Skill 根据你确认后的版本生成 PDF。JSON 结构见 [`assets/project-learning-guide.schema.json`](assets/project-learning-guide.schema.json)，Markdown 草稿模板见 [`assets/project-learning-guide-template.md`](assets/project-learning-guide-template.md)。批准前不会生成 PDF。批准后也可单独使用渲染器：

```bash
python3 scripts/render_project_learning_guide.py \
  career-miner-output/exports/project-learning-guide.json \
  --output-dir career-miner-output/exports
```

完整流程见 [`references/project-learning-pdf.md`](references/project-learning-pdf.md)。

## 许可证

Apache License 2.0。详见 [LICENSE](LICENSE)。
