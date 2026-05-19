# 二方包发布顺序参考（习惯四）

> 用于「二方包发布顺序提示」习惯。当用户问到二方包 / SDK / starter 的版本联动、发布顺序时，按本模板组织答案。

---

## 1. 项目与二方包关系

| # | 项目（依赖方） | 引用的二方包 | 原版本 | 目标版本 | 是否需先发布 | 备注 |
| - | --- | --- | --- | --- | --- | --- |
| 1 | service-order | payroll-boot-starter-util | 1.0.0 | 1.1.0 | 是 | 新增工具类 X |
| 2 | service-pay | payroll-boot-starter-util | 1.0.0 | 1.1.0 | 否（依赖 #1 发布完成） | 升级即可 |

## 2. 推荐发布顺序

按「自底向上」的顺序依次发布。被依赖的二方包必须**先发布到仓库**，依赖方再升级版本号。

1. **第 1 步**：发布 `payroll-boot-starter-util:1.1.0`（先 SNAPSHOT 联调，再打 RELEASE）。
2. **第 2 步**：在 `service-order` 的 `pom.xml` 中升级版本号至 `1.1.0`，跑回归测试，发布。
3. **第 3 步**：在 `service-pay` 的 `pom.xml` 中升级版本号至 `1.1.0`，跑回归测试，发布。

> 提示：如果有 N 个下游，**强烈建议**先选 1 个非核心服务做灰度验证再全量推。

## 3. 标准 Maven dependency 引用格式

### 直接写死版本号

```xml
<dependency>
    <groupId>com.cainiao.payroll</groupId>
    <artifactId>payroll-boot-starter-util</artifactId>
    <version>1.1.0</version>
</dependency>
```

### 通过 `<properties>` 管理版本（推荐）

```xml
<properties>
    <cn-payroll.starter.version>1.1.0</cn-payroll.starter.version>
</properties>

<dependency>
    <groupId>com.cainiao.payroll</groupId>
    <artifactId>payroll-boot-starter-util</artifactId>
    <version>${cn-payroll.starter.version}</version>
</dependency>
```

### 在父 POM `<dependencyManagement>` 中统一收口

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.cainiao.payroll</groupId>
            <artifactId>payroll-boot-starter-util</artifactId>
            <version>${cn-payroll.starter.version}</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

## 4. 发布前检查清单

- [ ] 二方包是否需要从 SNAPSHOT 升级为 RELEASE？是否走过对应分支策略？
- [ ] 是否存在循环依赖？（A 依赖 B，B 又依赖 A → 必须先重构）
- [ ] 二方包改动是否破坏了向后兼容？破坏性变更需要升大版本号（语义化版本）。
- [ ] 是否已通知所有下游业务方升级时间窗口？
- [ ] 是否已在测试环境完成端到端验证？

## 5. 常见坑位

- **本地 mvn install 跑通 ≠ 真发布成功**：务必确认包已推送到中央 / 内网 nexus 仓库。
- **下游使用了 LATEST / RELEASE 关键字**：会导致版本"漂移"，不可控，建议替换为固定版本。
- **`<dependencyManagement>` 与 `<dependencies>` 同时声明版本**：以子模块 `<dependencies>` 中的版本为准，容易踩坑。
