---
title: "Java and Truthy Checks"
date: 2024-06-24T00:00:00+00:00
tags: ["java"]
---

In most languages, you could just write a simple conditional statement by checking if the value of a variable is truthy or not, as shown below:
```python
value = ""

if value:
	print("value is truthy")
```
In java however, this is not supported. You have to explicitly write the condition you're testing for. In java, conditional tests must be a boolean (unlike the above code where the conditional test is actually a string, `value`) and so the only variable you can directly test without using a comparison operator is a boolean. 
```java
// can do
boolean isCodeBlock = true;

if (isCodeBlock) {
	System.out.println("This is a codeblock");
}

// CANNOT DO!
String name;

if (name) { // should be if (null != name) ...
	System.out.println("Name is not null");
}
```