# zh
Django 2.2.6
>本项目作为本人Django学习使用的第一个高级教程 
>以下为项目需求  最近在搭建博客 个人的心得与体会就不在此描述了


第二章 项目概述
2.1 产品描述
​ 赞乎是一个类似于知乎的知识问答社区，连接各行各业的用户。用户分享着彼此的知识、经验和见解，为中文互联网源源不断地提供多种多样的信息。

2.2 产品功能
​ 本产品为PC端，具有当今主流知识问答应用的功能，包括个人中心、动态、文章、问答、私信、消息通知、网站搜索，对外开放邮箱注册。

第三章 业务需求
3.1 总体需求
本产品不包含后台管理系统
网站所有内容需要用户登陆后才能访问
3.2 用户个人中心
3.2.1 登录/注册/退出等
​ 可以邮箱注册，使用第三方应用微信或Github注册登录，用户名登录，支持邮箱找回和重置密码。

3.2.2 个人信息
​ 包括昵称、邮箱、头像、简介、职称、城市、个人链接、微博链接、知乎链接、Github链接、LinkedIn链接，用户可以更新。

3.2.3 用户信息统计
​ 显示用户自网站注册日起，发表动态的数量，已发表文章的数量，参与评论的数量，提问的数量，回答问题的数量，用户的互动总数。

3.3 首页动态功能
3.3.1 动态列表页
最上方有“发表动态”按钮，每页显示20条动态
动态下有点赞和评论按钮
每条动态除内容外要显示用户头像、昵称、发表时间、赞和评论数量，用户互动后能自动更新数量
对于登录用户发表的动态，右上角显示删除按钮
3.3.2 发表动态
​ 发表动态字数不限，畅所欲言。

3.3.3 删除动态
​ 用户可以删除自己发表的动态。

3.3.4 用户点赞
​ 可以给自己和其他人点赞，也可以取消赞。

3.3.5 用户评论
​ 评论不能删除，除非状态被发表人删除。

3.4 文章模块
如下4个功能点中，第1、2、3各使用一页，页面上方有面包屑可以跳转；

3.4.1 浏览文章页
每页显示10篇文章
每篇文章显示标题、图片、内容的前100个字、发表人、发表时间、文章标签已经阅读全文的按钮
文章页要显示“写文章”和“草稿箱”按钮，云标签
3.4.2 文章详情页
每篇文章显示标题、图片、内容、发表人、发表时间
文章页要显示“写文章”和“编辑”按钮，云标签
文章下方有评论区
3.4.3 写文章
用户必填字段为标题、内容、文章图片、标签，标签支持多个使用英文逗号隔开

编辑文章内容时可Markdown实时预览

用户可将文章发表或保存为草稿，或者取消

3.4.4 保存草稿
​ 草稿箱与浏览文章页功能一样，不用之处在于用户只能看到自己保存的草稿。

3.4.5 评论文章
​ 用户评论时必填昵称、邮箱地址、内容，选填URL

3.5 问答模块
3.5.1 问答页
​ 页面上方有面包屑，下面是话题分类和提问按钮，下面是3个Tab栏目：待回答问题页、已回答问题页、所有问题页，每页显示20个问题；

​ 每个问题需要显示：回答的数量、问题的投票数量、标题、内容的前100个字符、提问者、提问时间、问题标签

3.5.2 问题详情页
​ 页面上方有面包屑，显示问题的所有回答

​ 问题需要显示：回答的数量、问题的投票数量、标题、内容的前100个字符、提问者、提问时间、问题标签；用户可以给问题投票，有提问按钮和回答按钮

​ 回答需要显示：回答的投票数、回答用户的头像和昵称、答案内容、回答时间、如果回答被接受显示对勾；用户可以给回答投票

3.5.3 用户提问
用户必填字段为标题、内容、标签，标签支持多个使用英文逗号隔开
编辑文章内容时可Markdown实时预览
用户可将问题发表或保存为草稿，或者取消
问题不能修改或删除
3.5.4 回答问题
​ 页面上方有面包屑，填写回答内容时可Markdown实时预览；回答不能修改或删除

3.5.5 给问题或回答投票
​ 显示票数=赞同数 - 反对数，用户可以赞同或反对，随时取消赞同或反对

3.5.6 提问者接受回答
​ 只能接受一个回答，接受后不能取消

3.6 私信功能
每页显示可私信的20个用户
对话框默认选中最近一次私信互动的用户
可与其他用户在线聊天
聊天内容显示头像、昵称、时间、内容，点击昵称可跳转至用户个人中心
3.7 消息通知
​ 当其它用户与我有如下互动时能接收到通知：

赞了我的状态
评论了我的动态或文章
收藏了我的文章
回答了我的提问
接受了我的回答
回复了我的评论
3.7.1 通知下拉框
​ 显示最近收到的5条消息通知，包括昵称、互动类型、互动对象、互动时间；有”查看所有通知“和”全部标为已读“按钮

3.7.2 未读通知列表
​ 显示所有的消息通知，有全部标为已读按钮；

​ 每条消息通知包括用户头像、昵称、互动类型、互动对象、互动时间，有”标为已读“按钮；

3.8 全站搜索
​ 可以搜索文章、动态、问题、用户、标签；

​ 文章搜索结果：显示文章图片、标题（可跳转）、内容的前100个字

​ 动态搜索结果：与首页的显示的动态信息一致

​ 问题搜索结果：与问答页显示的问题信息一致

​ 用户搜索结果：显示用户头像（可跳转）、昵称（可发邮件）、职位、城市

​ 标签搜索结果：显示被搜索到的标签
