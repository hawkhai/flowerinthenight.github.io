---
layout: page
title: 关于
author:
location:
categories:
tags:
toc:
toclistyle:
comments:
visibility:
mathjax:
mermaid:
glslcanvas:
codeprint:
permalink: /about/
---

{% include image.html url="/images/photo.jpg" caption="" width="300px" max_width="300px" align="right" %}

Hi, my name is hawkhai and welcome to my blog.

This is my personal web site.
I started to convert my notes into the web pages since mid 2020.
These are mostly fundamental information or tutorials to share with others.
I hope you find what you are looking for here.
And, I welcome any feedback on the contents and your suggestions.


## 为什么要写博客（Why write blog）

工作多年后，发现什么都没留下，一直忙于赶路，很多东西搞过，然后都忘记了。
稍微放慢一点，写写博客，用途多：

* 文档是代码的一部分，是同步更新的，代码改了，文档也要同步得到更新。
* 写文档和写单元测试类似，可以帮助我们写出逻辑更清晰，设计更合理的代码。
* 写作即思考，把学习的知识按自己的结构整理记录，方便日后查阅，还方便与他人交流。
* 短期看，写文档是浪费时间的；长期看，是节约时间的；更长期看，没有文档的代码甚至价值都不大，因为去理解它，重新用起来，需要的成本太大了。
* 能用图的就用图，不能用图就用表，不能用表，就用文字描述，读者就是未来完全忘光了的自己。

基于文档的知识迭代，比基于脑袋的迭代，更稳固、更可靠。正所谓：好记性不如烂笔头。

1. **边做边写文档，描述自己做的东西 --- 如果别人要改，成本能低一些；**
2. **关键的东西需要写清楚用法 --- 如果别人要用，不用去理解实现细节；**
3. **工程配置及编译会遇到的问题 --- 想跑起来，成本不用那么大。**

以前也做笔记，但是后来发现很多网址打不开了，你说找谁说理去？
这个博客系统加入了自动外链快照功能，博文里面包含的网址，会自动爬取快照存档。

> You do not need to leave your room. Remain sitting at your table and listen. Do not even listen, simply wait, be quiet still and solitary. The world will freely offer itself to you to be unmasked, it has no choice, it will roll in ecstasy at your feet.
> --- Franz Kafka


## 关于代码

程序的复杂度分两种：一种是这个逻辑本身就非常复杂，另一种是代码混乱和规模造成的复杂。

大部分时候，考验的是我们的基本功和知识储备。
同时用工整的代码和精巧的结构去对抗复杂，这就需要对设计模式有一定的了解。

客户端应用研发，大部分都是界面、回调、事件、线程之类，写来写去就那些东西。
深入一些的，也是一些算法啊什么的，开源的改吧改吧就能跑，更多的是考验快速学习的能力。

[^_^]: 有丰富经验后，旁征博引、触类旁通，才能驾驭更大更混乱的代码。


## Work history

* Software Engineer
  * Android
  * Windows
  * iOS
  * Linux
* And many others (mostly C/C++)...


## Spoken languages

* English??


## Others


## Contact

<div>
{% if site.email_address %}
<a href="mailto: {{ site.email_address }}">
    <span class="fa-stack fa-lg">
        <i class="fa fa-circle fa-stack-2x"></i>
        <i class="fa fa-envelope fa-stack-1x fa-inverse"></i>
    </span>
</a>
{% endif %}

{% if site.twitter_username %}
<a href="https://twitter.com/{{ site.twitter_username }}">
    <span class="fa-stack fa-lg">
        <i class="fa fa-circle fa-stack-2x"></i>
        <i class="fa fa-twitter fa-stack-1x fa-inverse"></i>
    </span>
</a>
{% endif %}

{% if site.github_username %}
<a href="https://github.com/{{ site.github_username }}">
    <span class="fa-stack fa-lg">
        <i class="fa fa-circle fa-stack-2x"></i>
        <i class="fa fa-github fa-stack-1x fa-inverse"></i>
    </span>
</a>
{% endif %}
</div>


## PGP public key
{% highlight shell %}

{% endhighlight %}

<hr class='reviewline'/>
<p class='reviewtip'><script type='text/javascript' src='{% include relref.html url="/assets/reviewjs/about.md.js" %}'></script></p>
<font class='ref_snapshot'>参考资料快照</font>

- [https://twitter.com/]({% include relref.html url="/backup/about.md/twitter.com/4fd9c9a2.html" %})
- [https://github.com/]({% include relref.html url="/backup/about.md/github.com/008ec445.html" %})
