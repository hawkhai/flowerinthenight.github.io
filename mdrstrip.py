#encoding=utf8
import re, os, sys
sys.path.append("../")
from pythonx.funclib import *
from pythonx.coderstrip import *

OPENFILE = "openfile" in sys.argv
AUTOFORMAT = "format" in sys.argv
REBUILD = "rebuild" in sys.argv
COPYRES = "copyres" in sys.argv

linktagli = (("{% include relref_bili.html %}]",    "bilibili]", "bilibili", "bilibili.com"),
             ("{% include relref_zhihu.html %}]",   "zhihu]",    "zhihu",    "zhihu.com"),
             ("{% include relref_cnblogs.html %}]", "cnblogs]",  "cnblogs",  "cnblogs.com"),
             ("{% include relref_csdn.html %}]",    "csdn]",     "csdn",     "csdn.net"),
             ("{% include relref_github.html %}]",  "github]",   "github",   "github.com|github.io"),
             ("{% include relref_github.html %}]",  "github]",   "github",   "github.com|github.io"),
             ("{% include relref_jianshu.html %}]", "jianshu]",  "jianshu",  "jianshu.com"),
             ("{% include relref_wiki.html %}]",    "wiki]",     "wiki",     "wikipedia.org"),
             ("{% include relref_weixin.html %}]",  "weixin]",   "weixin",   "weixin.qq.com"),
             ("{% include relref_keqq.html %}]",    "keqq]",     "keqq",     "ke.qq.com"),
             ("{% include relref_scriptol.html %}]","scriptol]", "scriptol", "scriptol.com"),
             ("{% include relref_khronos.html %}]", "khronos]",  "khronos",  "khronos.org"),
             ("{% include relref_gluon.html %}]",   "gluon]",    "gluon",    "gluon.ai"),
            )

def isHostIgnore(hostk):
    for tak, src, name, host in linktagli:
        if re.findall("^({})$".format(host), hostk):
            return True
        if re.findall("\\.{}$".format(host), hostk):
            return True
    for host in ("sunocean.life", "hawkhai.com",):
        if re.findall("^({})$".format(host), hostk):
            return True
        if re.findall("\\.{}$".format(host), hostk):
            return True
    return False

mdkeylist = """
categories
tags
location
comments
toclistyle
layout
visibility
mermaid
title
mathjax
glslcanvas
permalink
toc""".split()

g_snapcache = {}
g_untouched = {}
def buildSnapCache(rootdir):
    rootdir = os.path.normpath(rootdir)
    def mainfile(fpath, fname, ftype):
        fpath = os.path.normpath(fpath)
        if not re.findall("^[0-9a-f]{8}\\.", fname):
            return
        if fname.find(".selenium.png") != -1:
            return
        key = fname[:8]
        if not key in g_snapcache.keys():
            g_snapcache[key] = []
        g_snapcache[key].append(fpath)
        if not key in g_untouched.keys():
            g_untouched[key] = []
        g_untouched[key].append(fpath)
    searchdir(rootdir, mainfile)

def touchSnapCache(umd5, slocal):
    if umd5 in g_untouched.keys() and slocal in g_untouched[umd5]:
        g_untouched[umd5] = [i for i in g_untouched[umd5] if i != slocal]

def querySnapCache(umd5):
    if umd5 in g_snapcache.keys() and g_snapcache[umd5]:
        return readfile(g_snapcache[umd5][0])
    return None

def clearSnapCache():
    print("ClearSnapCache", len(g_untouched))
    for umd5 in g_untouched.keys():
        for x in g_untouched[umd5]:
            osremove(x)

def readfileIglist(fpath):
    li = readfile(fpath, "utf8").split("\n")
    li = [i.strip().split("#")[0].strip() for i in li if i.strip().split("#")[0].strip()]
    assert li, fpath
    return li

def backupUrlContent(fpath, url):
    for file in readfileIglist("mdrstrip_fileIgnore.txt"):
        if url.endswith(file):
            return
    assert not url.endswith(".exe"), url
    assert not url.endswith(".zip"), url
    # 有可能挂掉的网站，都稍微做一下备份。
    for host in readfileIglist("mdrstrip_hostIgnore.txt"):
        if url.startswith(host):
            return

    print(fpath, url)
    chrome = True # 可能有 js 代码，所以必须都用 Chrome 进行缓存
    chromeDialog = False
    for host in readfileIglist("mdrstrip_hostChrome.txt"):
        if url.startswith(host):
            chromeDialog = True
    mdname = os.path.split(fpath)[-1]
    uhost = url.split("//")[1].split("/")[0]
    umd5 = getmd5(url)
    ttype = ".html"
    local = os.path.join("backup", mdname, uhost, umd5 + ttype)
    ttype = calcType(ttype, url.split(uhost)[-1])
    slocal = os.path.join("backup", mdname, uhost, umd5[:8] + ttype)
    if os.path.exists(local):
        os.rename(local, slocal)

    if ttype.endswith(".pdf"): # pdf 下载
        chrome = False

    fdata = querySnapCache(umd5[:8])
    if fdata:
        writefile(slocal, fdata)
    else:
        fdata = netgetCacheLocal(url, timeout=60*60*24*1000, chrome=chrome, local=slocal, shotpath=slocal+".selenium.png", chromeDialog=chromeDialog)

        if url not in ("http://www.robots.ox.ac.uk/~az/lectures/ia/lect2.pdf",
                       "http://mstrzel.eletel.p.lodz.pl/mstrzel/pattern_rec/fft_ang.pdf",):
            assert len(fdata) < 1024*1024*1, len(fdata) / 1024.0 / 1024.0
    remote = "{}/{}/{}/{}".format("backup", mdname, uhost, umd5[:8] + ttype)
    touchSnapCache(umd5[:8], slocal)

    # 外链类型 断言...
    if not slocal.split(".")[-1] in ("pdf", "html", "git", "php", "c", "phtml", "cpp", "htm", "shtm",
                                     "ipynb", "py", "asp", "shtml", "aspx",):
        print(fpath, url)
        assert False, slocal
    return remote

g_orgremove = set()
def organizeClear():
    for key in g_orgremove:
        osremove(key)

def ffmpegConvert(fpath):
    if fpath.endswith(".264.mp4"): return
    tpath = fpath + ".264.mp4"
    if os.path.exists(tpath): return
    ffmpeg = r"C:\Program Files\ImageMagick-6.9.11-Q16-HDRI\ffmpeg.exe"
    cmdx = r"""
    "{}" -y -i "{}" -r 30000/1001
    -b:a 2M -bt 4M -vcodec libx264 -pass 1
    -coder 0 -bf 0 -flags -loop -wpredp 0
    -an "{}"
    """.format(ffmpeg, fpath, tpath)
    cmdx = " ".join(cmdx.split()).strip()
    ossystem(cmdx)

def organizeRes(ik, fpath, line):

    if ik in ("subsystem:windows /ENTRY:mainCRTStartup",):
        return line

    ikdir, ikfile = os.path.split(ik)
    if ikfile.find(".") == -1:
        ikfile = ikfile + ".jpg"
    iktype = ikfile.split(".")[-1].lower()
    if iktype == "mp4":
        ffmpegConvert(ik)

    if not COPYRES:
        assert os.path.exists(ik), fpath +"  "+ ik
        return line
    invisible = os.path.abspath(fpath).startswith(os.path.abspath("invisible")+"\\")
    fname = os.path.split(fpath)[-1]
    if fname.lower().endswith(".md"):
        fname = fname[:-3]
    if re.findall("^[0-9]{4}-[0-9]{2}-[0-9]{2}-", fname):
        fname = fname[:10].replace("-", "")[-6:]+"-"+fname[11:]
    if len(fname) > 32:
        fname = fname[:30]+"~"+getmd5(fname)[:2]

    tpath = os.path.join("assets", "images", fname, ikfile).lower()
    if invisible:
        tpath = os.path.join("invisible", "images", fname, ikfile).lower()
    if os.path.exists(ik):
        copyfile(ik, tpath)
        if os.path.abspath(ik) != os.path.abspath(tpath):
            g_orgremove.add(ik)
        # 同样大小的小图片先占位... lazyload
        sizepath = tpath + ".thumbnail.webp"
        if not os.path.exists(sizepath) and iktype in ("png", "jpg", "gif", "jpeg", "webp",):
            from PIL import Image
            img = Image.open(tpath)
            width, height = img.size
            if width > 100:
                img = img.resize((100, round(100.0*height/width)), Image.ANTIALIAS).convert("RGB")
                img = img.resize((width, height), Image.ANTIALIAS) # 恢复到原来大小，便于客户端排版。

                from PIL import Image, ImageFont, ImageDraw # 导入模块
                draw = ImageDraw.Draw(img, "RGBA") # 修改图片
                font = ImageFont.truetype(r"assets\logos\方正楷体_GB2312.ttf", size = 20)
                draw.rectangle(((0, 0), (img.size[0], 40)), fill=(0,0,0,127))
                draw.text((10, 10), u'图片加载中, 请稍后....', fill="#ffffff", font=font)
                #img.show()
                #exit(0)

            # 小于 100K...
            img.save(sizepath)
    else:
        assert False, ik

    iktype = ikfile.split(".")[-1].lower()
    if not iktype in ("pdf", "png", "jpg", "gif", "jpeg", "webp", "mp4", "zip"):
        print(ik, fpath, line)
        assert False, ik
    return line.replace(ik, tpath.replace("\\", "/"))

g_hostset = {}
def collectHost(fpath, line):

    reflist = []
    linesrc = line[:]

    regex = "(?:\"/(.*?)\")|(?:'/(.*?)')"
    li = re.findall(regex, line)
    for ik in li:
        ik = "".join(ik)
        if ik.endswith("/"):
            continue
        if len(ik) <= 2:
            continue

        kcontinue = False
        for src in ("/player.bilibili.com/",
                    "blog/", "source/shader/", "assets/glslEditor-0.0.20/"):
            if ik.startswith(src):
                kcontinue = True
        if kcontinue: continue

        if ik in ("images/photo.jpg",):
            continue
        if ik.startswith("source/"):
            continue
        if not os.path.isdir(ik):
            line = organizeRes(ik, fpath, line)

    regex = r"""(
                    (https?)://
                        ([a-z0-9\.-]+\.[a-z]{2,6})
                        (:[0-9]{1,4})?
                    (/[a-z0-9\&%_\./~=@–-]*)?
                    (\?[a-z0-9\&%_\./~=:-]*)?
                    (#[a-z0-9\&%_\./~=:-]*)?
                )"""

    regex = "".join(regex.split())
    li = re.findall(regex, line, re.IGNORECASE)
    if not li: return reflist, line
    for tx in li:
        url = tx[0]
        host = tx[2]
        checkz = line.split(url)
        for iline in checkz[1:]:
            checkli = ["", ")", "]", ">", " ", "*"]
            if url in ("https://msdl.microsoft.com/download/symbols",):
                checkli.append(";")
            if iline[:2] in ("{{",):
                continue
            if not iline[:1] in checkli:
                print(line)
                print(url)
                assert False, checkz
        assert not url.endswith("."), path +" "+ url
        remote = backupUrlContent(fpath, url)
        if remote:
            reflist.append([url, remote])

        if isHostIgnore(host):
            continue
        if not host in g_hostset:
            g_hostset[host] = 0
        g_hostset[host] += 1

    xline = line[:]
    for tak, src, name, host in linktagli:
        xline = xline.replace(tak, src)
    li = re.findall("<.*?>", xline)
    for tx in li:
        xline = xline.replace(tx, "")
    for tak, src, name, host in linktagli:
        # 视频要特别标注域名。
        li1 = re.findall(host, xline)
        li2 = re.findall(name+"\\]", xline)
        if len(li1) == len(li2):
            continue
        if xline.find("[")==-1 and xline.find("<")==-1 and xline.find("(")==-1:
            continue
        print(xline)
        print(li1)
        print(li2)
        openTextFile(fpath)
        assert False, linesrc
    return reflist, line

g_cnchar = []
g_cschar = []
g_enchar = []
g_tpset = set()
g_mdkeyset = set()
SNAPSHOT_HTML = "<font class='ref_snapshot'>参考资料快照</font>"
def removeRefs(fpath, lines):
    lineCount = len(lines)
    headIndex = -1
    for index in range(lineCount):
        i = lineCount-1 - index
        if not lines[i] or not lines[i].strip():
            continue
        if re.findall("^- \\[{}\\]\\({}\\)$".format(".*?", ".*?"), lines[i]): # \\[[0-9]+\\]
            continue
        if lines[i] == SNAPSHOT_HTML:
            headIndex = i
            break
        break

    if headIndex != -1:
        assert lines[headIndex-1] == "", "%r"%lines[headIndex-1]
        assert lines[headIndex-2] == "-----", "%r"%lines[headIndex-2]
        assert lines[headIndex-3] == "", "%r"%lines[headIndex-3]
        lines = lines[:headIndex-3]
    return lines

def appendRefs(fpath, lines):
    reflist = []

    for index, line in enumerate(lines):
        ireflist, line = collectHost(fpath, line)
        lines[index] = line
        if ireflist:
            reflist.extend(ireflist)

    if reflist:
        lines.append("")
        lines.append("-----")
        lines.append("")
        lines.append(SNAPSHOT_HTML)
        lines.append("")
        lines.append("")
        urlset = set()
        count = 0
        for url, remote in reflist:
            if url in urlset: continue
            urlset.add(url)
            count = count + 1
            from urllib.parse import unquote
            remote = "{% " + ("include relref.html url=\"/%s\"" % (remote,)) + " %}"
            lines.append("- [{}]({})".format(url, remote)) # count
        lines.append("")
    return lines

def mainfile(fpath, fname, ftype):
    checkfilesize(fpath, fname, ftype)

    ftype = ftype.lower()
    errcnt = 0

    warnCnEnSpace    = ftype in ("md", "php", "html", "htm", "vsh", "fsh",) # 英文中文空符检查
    warnTitleSpace   = ftype in ("md",) # 标题前后空行检查
    warnIndentSpace  = ftype in ("md", "php", "scss", "vsh", "fsh",) # 缩进检查
    isMdFile         = ftype in ("md",)
    isSrcFile        = ftype in ("md", "php", "html", "htm", "js", "css", "scss", "svg", "py", "vsh", "fsh",)
    keepStripFile    = ftype in ("svg",) or fname in ("gitsrc.html",) or re.findall("^relref[a-z_]*\\.html$", fname)

    if fpath.find("\\winfinder\\") != -1:
        isSrcFile = isSrcFile or ftype in ("h", "cpp", "rc", "c",)

    if not isSrcFile:
        if fpath.find("\\_site\\") != -1:
            g_tpset.add(ftype)
        return

    if isMdFile:
        fdata = readfile(fpath, True).strip()
        if fdata.startswith("---"):
            kvlist = fdata.split("---")[1].strip().split("\n")
            for kv in kvlist:
                kv = kv.strip()
                key, value = kv.split(":", 1)
                key = key.strip()
                value = value.strip()
                g_mdkeyset.add(key)

    if fpath.find("\\_site\\") != -1:
        return

    def linerstrip(line):
        if isMdFile:
            for tak, src, name, host in linktagli:
                # 移除多余空格
                line = line.replace("  "+tak, tak)
                line = line.replace(" "+tak, tak)
                # 格式化。
                line = line.replace(tak, " "+tak)
                line = line.replace(src, tak)
                line = line.replace("[ "+tak, "["+name+" "+tak)
            line = line.replace(" ——", "——").replace(" ——", "——")
            line = line.replace("—— ", "——").replace("—— ", "——")
            line = line.replace("——", " —— ")
        return line.rstrip()

    print(fpath)
    try:
        lines = readfileLines(fpath, False, False, "utf8")
    except Exception as ex:
        openTextFile(fpath)
        raise ex
    lines = removeRefs(fpath, lines)
    lines = [linerstrip(line) for line in lines]
    lines.append("")
    lines.append("")
    while len(lines) >= 2 and not lines[-1] and not lines[-2]:
        lines = lines[:-1]
    while len(lines) >= 1 and not lines[0]:
        lines = lines[1:]

    if keepStripFile:
        while len(lines) >= 1 and not lines[-1]:
            lines = lines[:-1]

    if isMdFile:
        lines = appendRefs(fpath, lines)

    codestate = False
    chartstate = False
    for index, line in enumerate(lines):

        preline = lines[index - 1] if index > 0 else ""
        nextline = lines[index + 1] if index < len(lines)-1 else ""

        tagregex = "^\\s*[#]+ "
        tagregexk = "^\\s*[#]+\\s{2,}"
        prelinetag = re.findall(tagregex, preline)
        nextlinetag = re.findall(tagregex, nextline)
        if warnTitleSpace:
            assert not re.findall(tagregexk, preline), preline

        if re.findall("^\\s*[*-]+ ", line):
            idtcnt = 2
        else:
            idtcnt = 4

        cnsign  = "‘’“”"
        cnregex = "\u4e00-\u9fa5"

        for ch in line:
            ordch = ord(ch)
            regch = "\\u%04x"%(ordch)
            if ordch <= 0x7F or isDiacritic(ch):
                g_enchar.append(ch)
                continue
            if ordch >= 0x4e00 and ordch <= 0x9fa5:
                if cnregex.find(regch) == -1:
                    cnregex += regch
                if g_cnchar.count(ch) == 0:
                    g_cnchar.append(ch)
            else:
                if cnsign.find(regch) == -1:
                    cnsign += regch
                if g_cschar.count(ch) == 0:
                    g_cschar.append(ch)
        cnregex += cnsign

        if line.find("\xa0") != -1 and not fname in ("glslEditor.min.js",):
            print("xspace", fpath, line)
            errcnt += 1

        #liw = re.findall("[{}]+".format(cnregex,), line, re.IGNORECASE)
        #lia = re.findall("[^{}]+".format(cnregex,), line, re.IGNORECASE)

        linec = line
        for itmp in re.findall("\\$\\$.*?\\$\\$", line): # 忽略数学公式
            linec = linec.replace(itmp, "$$$$")
        for itmp in re.findall("“.*?”", line): # 忽略双引号
            linec = linec.replace(itmp, "“”")

        for itmp in ('"Web前端"',):
            linec = linec.replace(itmp, "\"\"")

        linec = linec.replace('caption="', 'caption=" ')

        lix1 = re.findall("[{}][^{} *]".format(cnregex, cnregex), linec, re.IGNORECASE)
        lix2 = re.findall("[^{} *][{}]".format(cnregex, cnregex), linec, re.IGNORECASE)
        lix = []
        lix.extend(lix1)
        lix.extend(lix2)

        cnsignregex = "[{}]".format(cnsign)
        for ix in lix:
            cx, cy = ix
            if re.findall(cnsignregex, cy) or re.findall(cnsignregex, cx):
                continue
            if cy in "-<]" or cx in "->[":
                continue

            if chartstate:
                continue

            if cx in ("\"", "[") and (" "+line).count(" "+ix) == 1:
                continue
            if cy in ("\"", "]", ",") and (line+" ").count(ix+" ") == 1:
                continue

            if cx in ("(", ) and (" \\"+line).count(" \\"+ix) == 1:
                continue
            if cy in ("\\", ) and (line+") ").count(ix+") ") == 1:
                continue

            if cx in ("\"",) and ("["+line).count("["+ix) == 1:
                continue
            if cy in ("\"",) and ((line+"]").count(ix+"]") == 1 or (line+",").count(ix+",") == 1):
                continue

            if cy in (".") and (line.count(ix+"rar") == 1 or line.count(ix+"zip") == 1):
                continue

            if not warnCnEnSpace:
                continue

            if codestate:
                if cy in "\":" or cx in "\":":
                    continue

                if line.startswith("print ("):
                    continue

            print("[%d]"%(index+1), ix, cx, cy, "\t", line)
            errcnt += 1
            if AUTOFORMAT:
                line = line.replace(ix, cx+" "+cy)
                lines[index] = line

        fxline = "".join(line.split())
        if fxline.startswith("<divclass=\"mermaid\"") and not chartstate:
            chartstate = True
        if fxline.startswith("</div>") and chartstate:
            chartstate = False

        if fxline.startswith("{%highlight"):
            codestate = True
            continue
        if fxline.startswith("{%endhighlight%}"):
            codestate = False
            continue

        if fxline.startswith("```") and not codestate:
            codestate = True
            continue
        if fxline.startswith("```") and codestate:
            codestate = False
            continue

        if codestate:
            continue

        if warnTitleSpace and (prelinetag or nextlinetag):
            if line:
                openTextFile(fpath)
                assert False, "{}:{} {}".format(fpath, index+1, line)

        countspace = getLeftSpaceCount(line if warnIndentSpace else line.replace("\t", " "*4))
        if countspace > 12 or countspace % idtcnt == 0:
            pass # ok
        elif warnIndentSpace:
            openTextFile(fpath)
            assert False, "{}:{} \"{}\"".format(fpath, index+1, line)

    page = "\r\n".join(lines)
    while page.find("\r\n" * 3) != -1:
        page = page.replace("\r\n" * 3, "\r\n" * 2)

    codereg = "\\{\\%\\s*highlight.*?\\{\\%\\s*endhighlight\\s*\\%\\}"
    codeli1 = re.findall(codereg, page, re.MULTILINE | re.IGNORECASE | re.DOTALL)

    coderegz = "```.*?```"
    codeli1z = re.findall(coderegz, page, re.MULTILINE | re.IGNORECASE | re.DOTALL)

    if warnTitleSpace:
        page = page.replace("\r\n"*2+"### ", "\r\n"*3+"### ")
        page = page.replace("\r\n"*2+"## ",  "\r\n"*3+"## ")
        page = page.replace("\r\n"*2+"# ",   "\r\n"*3+"# ")

    codeli2 = re.findall(codereg, page, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    for i in range(len(codeli1)):
        page = page.replace(codeli2[i], codeli1[i])

    codeli2z = re.findall(coderegz, page, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    for i in range(len(codeli1z)):
        page = page.replace(codeli2z[i], codeli1z[i])

    writefile(fpath, page.encode("utf8"))
    return errcnt

def viewchar(lichar, xfile, xmin, xmax):
    li = list(set("".join(lichar)))
    li.sort()
    page = ""
    minv, maxv = 1024, 0
    for index, tchar in enumerate(li):
        page += tchar
        if (index + 1) % 50 == 0:
            page += "\r\n"
        if isDiacritic(tchar):
            continue
        minv = min(minv, ord(tchar))
        maxv = max(maxv, ord(tchar))
    tempfile = os.path.join("tempdir", xfile)
    writefile(tempfile, page.encode("utf8"))

    if OPENFILE:
        openTextFile(tempfile)
    print(minv, maxv)
    print([("%04x"%ord(k), k) for k in li[:5]]),
    print([("%04x"%ord(k), k) for k in li[-5:]])
    assert xmin <= minv and maxv <= xmax

def mainfilew(fpath, fname, ftype):
    if checklog(__file__, fpath) and not REBUILD:
        # print("cached", fpath)
        return 0
    removelog(__file__, fpath)
    errcnt = mainfile(fpath, fname, ftype)
    if errcnt == 0:
        savelog(__file__, fpath)
    return errcnt

g_checkfilesize = set()
def checkfilesize(fpath, fname, ftype):
    fmd5 = getFileMd5(fpath)
    if not g_checkfilesize:
        for ifmd5 in readfileIglist("mdrstrip_bigfiles.txt"):
            g_checkfilesize.add(ifmd5)

    if not (fmd5 in g_checkfilesize):
        size = os.path.getsize(fpath) / 1024.0 / 1024.0
        if size >= 1.0:
            print(getFileMd5(fpath), "#", fpath, "#", "%.1f MB"%size)
            g_checkfilesize.add(fmd5)

            if ftype in ("gif",):
                from pythonx import pygrab
                pygrab.gifbuildwebp(fpath)

            openTextFile("mdrstrip_bigfiles.txt")
            assert False, "大文件最好不要入库..."

def main():
    print(parsePythonCmdx(__file__))
    removedirTimeout("tempdir")
    clearemptydir("tempdir")
    buildSnapCache("backup")

    CHECK_IGNORE_LIST = (
        "backup", "tempdir", "_site",
        "Debug", "Release", ".vs", "opengl-3rd",
        "UserDataSpider",
        )
    searchdir(".", checkfilesize, ignorelist=CHECK_IGNORE_LIST)
    searchdir("backup", checkfilesize, ignorelist=CHECK_IGNORE_LIST)

    searchdir(".", mainfilew, ignorelist=(
        "backup", "d2l-zh", "mathjax", "tempdir", "msgboard",
        "Debug", "Release", ".vs", "openglcpp", "opengl-3rd",
        "UserDataSpider",
        ), reverse=True)
    if REBUILD:
        clearSnapCache()
        clearemptydir("images")
        clearemptydir("source")
        organizeClear()

    global g_cschar
    global g_tpset

    viewchar(g_cnchar, "cnfile.txt", 0x80, 0x7FFFFFFF)
    viewchar(g_cschar, "csfile.txt", 0x80, 0x7FFFFFFF)
    viewchar(g_enchar, "enfile.txt", 0x0,  0x7F)

    print(LINE_SEP_SHORT)
    g_cschar = list(set(g_cschar))
    g_cschar.sort()
    print("".join(g_cschar))
    imgset  = ("jpeg", "jpg", "png", "gif", )
    fontset = ("eot", "ttf", "woff", "svg", "woff2", )
    codeset = ("cc", "js", "txt", "xml", "css", "mk", "lock", "zip", "makefile", "scss",)
    g_tpset -= set(imgset)
    g_tpset -= set(fontset)
    g_tpset -= set(codeset)
    print(g_tpset)
    print(g_mdkeyset)

    hostlist = sorted(g_hostset.items(), key=lambda x: x[1], reverse=True)
    print(hostlist)
    for hostx in hostlist[:10]:
        print(hostx)

if __name__ == "__main__":
    main()
    print(parsePythonCmdx(__file__))
    os.system(r"cd invisible & python tempd.py encrypt")
