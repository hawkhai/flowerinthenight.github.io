#encoding=utf8
import re, os, sys
sys.path.append("../")
from pythonx.funclib import *

OPENFILE = "openfile" in sys.argv
AUTOFORMAT = "format" in sys.argv

# 在西歐、北歐及東歐國家常用的字母，帶變音符，和一般英文字母不同。
DIACRITIC = """
À Á Â Ã Ä Å Æ Ā Ă Ą
Ç Ć Ĉ Ċ
Ð Ď Đ
È É Ê Ë Ē Ė Ę Ě Ə
Ĝ Ġ Ģ
Ĥ Ħ
Ì Í Î Ï Ī Į Ĳ
Ĵ
Ķ
Ļ Ł
Ñ Ń Ņ Ň
Ò Ó Ô Õ Ö Ø Ő Œ
Ŕ Ř
ẞ Ś Ŝ Ş Š Ș Þ
Ţ Ť Ț
Ù Ú Û Ü Ū Ŭ Ů Ű Ų
Ŵ
Ý Ŷ
Ÿ Ź Ż Ž
à á â ã ä å æ ā ă ą
ç ć ĉ ċ
ð ď đ
è é ê ë ē ė ę ě ə
ĝ ġ ģ
ĥ ħ
ì í î ï ī į ĳ
ĵ
ķ
ļ ł
ñ ń ņ ň
ò ó ô õ ö ø ő œ
ŕ ř
ß ś ŝ ş š ș þ
ţ ť ț
ù ú û ü ū ŭ ů ű ų
ŵ
ý ŷ
ÿ ź ż ž"""
DIACRITIC = "[{}]".format("".join(DIACRITIC.split()))

def getLeftSpaceCount(line):
    line = line[:]
    assert not line.startswith("\t"), line
    count = 0
    while line and line[0] == ' ':
        line = line[1:]
        count += 1
    return count

def createCnFile():
    page = b""
    ordch = 0x4e00
    count = 0
    while ordch <= 0x9fa5:
        ch = chr(ordch)
        ordch += 1
        page += ch.encode("utf8")
        count += 1
        if count % 50 == 0:
            page += b"\r\n"
    tempfile = tempfile = os.path.join("tempdir", "tempfile.txt")
    writefile(tempfile, page)
    openTextFile(tempfile)
#createCnFile()

g_cnchar = []
g_cschar = []
g_enchar = []
g_tpset = set()
g_mdkeyset = set()
def mainfile(fpath, fname, ftype):

    if fpath.find("\\backup\\") != -1:
        return
    if fpath.find("\\d2l-zh\\") != -1:
        return

    ftype = ftype.lower()
    if not ftype in ("md", "py", "php", "html", "htm",):
        if fpath.find("\\_site\\") != -1:
            g_tpset.add(ftype)
        return

    if ftype in ("md",):
        fdata = readfile(fpath, True).strip()
        if fdata.startswith("---"):
            kvlist = fdata.split("---")[1].strip().split("\n")
            for kv in kvlist:
                kv = kv.strip()
                key, value = kv.split(":", 1)
                key = key.strip()
                value = value.strip()
                g_mdkeyset.add(key)

    warnCnEnSpace    = ftype in ("md", "php", "html", "htm",)
    warnMdTitleSpace = ftype in ("md",)
    warnIndentSpace  = ftype in ("md", "py", "php",)

    if fpath.find("\\_site\\") != -1:
        return

    print(fpath)
    lines = readfileLines(fpath, False, False, "utf8")
    lines = [line.rstrip() for line in lines]
    lines.append("")
    lines.append("")
    while len(lines) >= 2 and not lines[-1] and not lines[-2]:
        lines = lines[:-1]
    while len(lines) >= 1 and not lines[0]:
        lines = lines[1:]

    if fname in ("relref.html",):
        while len(lines) >= 1 and not lines[-1]:
            lines = lines[:-1]

    codestate = False
    for index, line in enumerate(lines):
        count = getLeftSpaceCount(line)
        preline = lines[index - 1] if index > 0 else ""
        nextline = lines[index + 1] if index < len(lines)-1 else ""

        tagregex = "^\\s*[#]+ "
        tagregexk = "^\\s*[#]+\\s{2,}"
        prelinetag = re.findall(tagregex, preline)
        nextlinetag = re.findall(tagregex, nextline)
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
            if ordch <= 0x7F or re.findall(DIACRITIC, ch):
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

        if line.find("\xa0") != -1:
            print("xspace", fpath, line)

        #liw = re.findall("[{}]+".format(cnregex,), line, re.IGNORECASE)
        #lia = re.findall("[^{}]+".format(cnregex,), line, re.IGNORECASE)

        linec = line
        for itmp in re.findall("\\$\\$.*?\\$\\$", line): # 忽略数学公式
            linec = linec.replace(itmp, "$$$$")

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

            if cx in ('"', "[") and (" "+line).count(" "+ix) == 1:
                continue
            if cy in ('"', "]", ",") and (line+" ").count(ix+" ") == 1:
                continue
            if cx in ('"',) and ("["+line).count("["+ix) == 1:
                continue
            if cy in ('"',) and (line+"]").count(ix+"]") == 1:
                continue

            if not warnCnEnSpace:
                continue

            if codestate:
                if cy in "\":" or cx in "\":":
                    continue

                if line.startswith("print ('"):
                    continue

            print("[%d]"%(index+1), ix, "\t", line)
            if AUTOFORMAT:
                line = line.replace(ix, cx+" "+cy)
                lines[index] = line

        fxline = "".join(line.split())
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

        if warnMdTitleSpace and (prelinetag or nextlinetag):
            if line:
                openTextFile(fpath)
                assert False, "{}:{} {}".format(fpath, index+1, line)

        if count > 12 or count % idtcnt == 0:
            pass # ok
        elif warnIndentSpace:
            openTextFile(fpath)
            assert False, "{}:{} {}".format(fpath, index+1, line)

    page = "\r\n".join(lines)
    while page.find("\r\n" * 3) != -1:
        page = page.replace("\r\n" * 3, "\r\n" * 2)

    codereg = "\\{\\%\\s*highlight.*?\\{\\%\\s*endhighlight\\s*\\%\\}"
    codeli1 = re.findall(codereg, page, re.MULTILINE | re.IGNORECASE | re.DOTALL)

    coderegz = "```.*?```"
    codeli1z = re.findall(coderegz, page, re.MULTILINE | re.IGNORECASE | re.DOTALL)

    if warnMdTitleSpace:
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

def viewchar(lichar, xfile, xmin, xmax):
    li = list(set("".join(lichar)))
    li.sort()
    page = ""
    minv, maxv = 1024, 0
    for index, tchar in enumerate(li):
        page += tchar
        if (index + 1) % 50 == 0:
            page += "\r\n"
        if re.findall(DIACRITIC, tchar):
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

def main():
    print(parsePythonCmdx(__file__))
    searchdir(".", mainfile)
    global g_cschar
    global g_tpset

    viewchar(g_cnchar, "cnfile.txt", 0x80, 0x7FFFFFFF)
    viewchar(g_cschar, "csfile.txt", 0x80, 0x7FFFFFFF)
    viewchar(g_enchar, "enfile.txt", 0x0,  0x7F)

    print(LINE_SEP_SHORT)
    g_cschar = list(set(g_cschar))
    g_cschar.sort()
    print("".join(g_cschar))
    imgset  = ('jpeg', 'jpg', 'png', 'gif', )
    fontset = ('eot', 'ttf', 'woff', 'svg', 'woff2', )
    codeset = ('cc', 'js', 'txt', 'xml', 'css', 'mk', 'lock', 'zip', 'makefile', )
    g_tpset -= set(imgset)
    g_tpset -= set(fontset)
    g_tpset -= set(codeset)
    print(g_tpset)
    print(g_mdkeyset)

if __name__ == "__main__":
    main()
