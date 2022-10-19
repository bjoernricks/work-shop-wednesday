## General

* Python is a dynamic scripting language
* Python allows for object oriented programming (OOP) but also for functional programming
  * It is possible to define classes with methods
  * Instances of classes are called objects
* Python uses duck typing
  * *“If it walks like a duck, and it quacks like a duck, then it must be a duck.”*
  * It's based on so called *Protocols*
  * Protocols define the availability of specific methods and their signatures
  * Methods of Protocols are (mostly) *dunder* methods
    * dunder -> double underscore
    * `__foo__(...)`
    * Most famous the constructor method `def __init__(self)`
* Functions (and therefore also methods) return `None` implicitly if no return
  statement is defined or if it has no value.
  ```python
  def foo():
    print("foo")
  ```
  is the same as
  ```python
  def foo():
    print("foo")
    return
  ```
  is the same as
  ```python
  def foo():
    print("foo")
    return None
  ```
