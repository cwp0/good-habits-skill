# Java 注释规范参考（习惯六）

> 用于「Java 注释规范」习惯。当 Agent 在 Java 文件中**新建**类 / 枚举 / 接口 / 方法 / 静态变量 / 实例变量时，按本文档的格式补全 Javadoc 与行内注释。

---

## 0. 范围与原则

- **仅对新建元素强制补注释**。已有完整注释的元素**不重写**，避免无谓 diff。
- **方法内变量**仅在「变量含义不直观」时加行内注释；变量名已自解释（如 `userId`、`totalCount`）则**不加**。
- **占位符**统一使用方括号 `[xxx]` 表示需替换的内容，例如 `[类的描述]`。
- **作者名**默认填 `鹤童`。如果 skill 维护者需要替换，改本文件一处即可，所有样例同步生效（Agent 应以本文件为唯一事实源）。
- **日期**取**当前本地时间**，格式严格为 `YYYY/MM/DD HH:mm`（24 小时制，例如 `2026/05/18 14:32`）。

---

## 1. 类

```java
/**
 * @author 鹤童
 * @desc [类的描述]
 * @date [当前日期，格式：YYYY/MM/DD HH:mm]
 */
public class Demo {

}
```

## 2. 枚举

```java
/**
 * @author 鹤童
 * @desc [枚举的描述]
 * @date [当前日期，格式：YYYY/MM/DD HH:mm]
 */
public enum Demo {
    DEMO;
}
```

## 3. 接口

```java
/**
 * @author 鹤童
 * @desc [接口的描述]
 * @date [当前日期，格式：YYYY/MM/DD HH:mm]
 */
public interface Demo {
    void function();
}
```

## 4. 方法

```java
    /**
     * [方法的描述]
     *
     * @param param1 [参数1的描述]
     * @param param2 [参数2的描述]
     * @param param3 [参数3的描述]
     * @return [返回值的描述]
     */
    List<String> function(String param1, String param2, String param3);
```

要点：
- 首行写方法描述（一句话，句末不加句号亦可，但需具备完整语义）。
- 描述与 `@param` 之间空一行。
- 每个参数都要有 `@param`，按方法签名顺序列出。
- 非 `void` 方法必须有 `@return`；`void` 方法不写 `@return`。
- 抛出受检异常时建议补 `@throws`（非强制，但推荐）。

## 5. 静态变量

```java
/**
 * [静态变量的描述]
 */
public static final int DEMO = 1;
```

## 6. 实例变量

```java
/**
 * [实例变量的描述]
 */
public int demo;
```

## 7. 方法内变量

```java
public void function() {
    // [方法内变量的描述]
    int demo = 1;
}
```

要点：
- **仅在变量含义不直观时**才加行内注释，否则省略。
- 反例（不要这样写）：

  ```java
  // 用户ID
  String userId = ctx.getUserId();
  ```

  变量名 `userId` 已经自解释，注释纯属噪声，应删除。

- 正例（应当这样写）：

  ```java
  // 兼容历史数据：旧版接口返回的金额单位是分，需手动除以 100 转为元
  BigDecimal amount = legacyResponse.getAmount().divide(BigDecimal.valueOf(100));
  ```

  此处的「为什么这样做」无法从代码本身看出，加注释是有价值的。

---

## 8. 与其他习惯的关系

- **习惯一（先方案后动手）优先**：用户提需求时仍要先按习惯一出方案，方案通过后**动手写代码时**再按本文档的格式落注释。
- **习惯三（自动记录 Q&A）正交**：写完代码记录 Q&A 时，本规范不影响 Q&A 文件的内容。

---

## 9. 检查清单（Agent 自查）

写完一段 Java 代码后，按下列清单自查：

- [ ] 新建的每一个类 / 枚举 / 接口都带 `@author / @desc / @date` 三行 Javadoc。
- [ ] `@date` 用的是**当次操作的本地时间**，不是占位符。
- [ ] 新建的每一个方法都带方法描述 + `@param`（每参一行）+ `@return`（非 void）。
- [ ] 新建的每一个静态变量、实例变量都带单行 Javadoc。
- [ ] 方法内变量只对「含义不直观」的加了行内注释，未给已自解释的变量加注释。
- [ ] 没有重写已有完整注释的元素，diff 干净。
