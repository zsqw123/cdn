# HealthInfoAutoReport

[![构建状态](https://zsqw123.coding.net/badges/autotmp/job/483170/build.svg)](https://coding.net)

## First, u need 2 bind u wx with u phone num

**Remind: First, u need post u temp least 1 time.**

open wx, scan this:

![wx](https://cdn.jsdelivr.net/gh/zsqw123/cdn@master/picCDN/20210202105525.png)

bind:

**Notice: u wx binded num must same with u input below.**

**If u can't, ask u leader for help.**

![bind](https://cdn.jsdelivr.net/gh/zsqw123/cdn@master/picCDN/20210202105734.png)

if binded, u will see a new QR code, scan and follow it.

![newQR](https://cdn.jsdelivr.net/gh/zsqw123/cdn@master/picCDN/20210202110147.png)

then use ur leader's way to report once

## Second: Choose one of the following to run auto report

### 1. Through Remote Environment: Github Actions

1. star and fork this repo.
2. set your own those 2 Actions secrets: NUM, PWD
3. enable action and commit anything or wait actions auto run.

### 2. Through Local Environment: Python 3.6+

```powershell
pip install requests
pip install beautifulsoup4
pip install lxml
```

Run this:

```powershell
python actions.py account pwd
```
## Notice

- If u want 2 c your class completion, For example: 0313191, u can by fllowing link:
```text
https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/ajaxExcelByBh.jsp?bh=0313191

this link is REALTIME.
```

- u need post u temp least 1 time.
- u can run `multi.py` by same way in your local machine to complete your missing.
- Using this project means you agree to [this](NOTICE.md)
