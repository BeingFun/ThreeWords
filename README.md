# ThreeWords

## 初衷：相信文字的力量

## 简介

本程序可以为 Windows 系统桌面壁纸自动添加一句你可能喜欢的文字。

## 1. 使用说明

下载压缩包后解压即可使用  
可执行程序位于: ThreeWords\\bin\\ThreeWords.exe 双击即可运行  
用户自定义配置文件位于: ThreeWords\\config\\config.ini  
程序异常 log 位于根目录: Error.log 欢迎将运行中的 bug 以 issues 形式提交

## 2. 配置说明

### 基础配置

| 参数                   | 类型   | 默认值  | 说明                                               
|----------------------|------|------|--------------------------------------------------|
 START_WITH_SYSTEM    | bool | True | 是否开机自启 True: 开启 False: 关闭
 UPDATE_PERIOD | int  | 60   | 文字/图像刷新时间间隔， 单位: 分钟                                   

### 背景图像配置

| 参数                     | 类型     | 默认值     | 说明                                                                          
|------------------------|--------|---------|-----------------------------------------------------------------------------|
 BACKGROUND_IMAGES_PATH | string | Default | 桌面壁纸来源,有三种配置方式: Default,Path,Bing<br>Default 使用 ThreeWords 默认附带的图片,如 BACKGROUND_IMAGES_PATH = Default<br>Path 使用 用户配置的文件夹路径,如 BACKGROUND_IMAGES_PATH = D:\xxx\xxx\images<br>Bing 使用 必应每日壁纸,如 BACKGROUND_IMAGES_PATH = Bing
 OPEN_BACKGROUND_UPDATE | bool | False | 是否开启桌面背景图片定时更新 True: 开启 False: 关闭

### 文本配置

| 参数            | 类型     | 默认值           | 说明                                                                   
|---------------|--------|---------------|----------------------------------------------------------------------|
OPEN_TEXT_UPDATE    | bool | True       | 是否开启文字定时更新 True: 开启 False: 关闭
 TEXT_STYLE    | string | Default       | 文字风格设置，默认值为随机风格。<br>目前支持的分类: 动画、漫画、游戏、文学、原创、来自网络、其他、影视、诗词、网易云、哲学、抖机灵。<br>支持多风格复选，如: TEXT_STYLE = 文学 and 诗词 and 动画
 TEXT_FROM     | bool   | False         | 是否显示文字出处，如:<br>关关雎鸠，在河之洲。<br>                                ----《诗经/关雎》  
 TEXT_POSITION | tuple  | (-1, -1)      | 文字起始位置，单位: 像素 默认值为图片中间位置<br>用户配置示例: (50,60) 表示文字从 距离屏幕顶部 60 左边 50 的位置开始绘制文字。                                             
 FONT_COLOR    | tuple  | (250,250,250) | 文字颜色设置，支持 RGB 格式                                                       
 FONT_SIZE     | int    | 72            | 字体大小                                                                 
 FONT_TYPE     | string | simkai.ttf    | 字体类型，请设置自己系统支持的字体                                                    

[你可以参考的常用字体列表](https://blog。csdn。net/pizi0475/article/details/5404798?utm_medium=distribute。pc_relevant。none-task-blog-2~default~baidujs_baidulandingword~default-5-5404798-blog-108802333。235^v27^pc_relevant_3mothn_strategy_and_data_recovery&spm=1001。2101。3001。4242。4&utm_relevant_index=8)

[你可以参考的RGB色彩](http://www。tbfl。store/dev/rgb。html)

## 3. 常见问题

Q: 为什么没有随系统开机自启动？

A: 请尝试以管理员权限运行程序一次。

## 开发手册

TODO

## 开源协议

TODO
