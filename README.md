# fduxk

简单的写了个选课的脚本。你需要做的是：
- 手动查看目录下的图片，输入验证码（尝试了好多个识别软件，都不太好用，自己又不想训，那就先手动收入吧，会话可以保存很久，输一次也还行）；
- 更改loginName以及loginPwd；
- 查看课程的信息，并更改course_data中的数据，信息可在网页端打开控制台，刷新网页后的Network中的loadGgxxkCourseInfo.do文件查看（你想选的课）bjdm、bqmc信息；
- lx暂时没有仔细排查，目前认为是以下信息：

| lx数值 | 含义 |
| :--: | :--: |
| 1 | 政治选修课 or 第一外国语 |
| 2 | 学位基础课 or 学位专业课 or 专业选修课 |
| 4 | haveCourses(已选课？) |
| 5 | retakeCourses（重修课程） |
| 9 | 公共选修课 |
| 10 | 其他选修课 |

以下几个不明含义，可能是本科生的课程类型，请自行推测。

| lx数值 | 含义            |
| :----- | --------------- |
| 7      | commonCourses   |
| 8      | academicCourses |
| 99     | openedCourses   |

