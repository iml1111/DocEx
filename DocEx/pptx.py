try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

NAMESPACE = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
TEXT = NAMESPACE + 't'


def get_pptx_text(filename):
    document = zipfile.ZipFile(filename)
    text_list = []

    # 각 슬라이드 name들 추출
    nums = []
    for d in document.namelist():
        if d.startswith("ppt/slides/slide"):
            nums.append(int(d[len("ppt/slides/slide"):-4]))

    s_format = "ppt/slides/slide%s.xml"
    slide_name_list = [s_format % x for x in sorted(nums)]

    # 슬라이드를 순회하며 텍스트 추출
    for slide in slide_name_list:
        xml_content = document.read(slide)
        tree = XML(xml_content)
        
        slide_text_list = []
        for node in tree.getiterator(TEXT):
            if node.text:
                slide_text_list.append(node.text)
        
        text_list.append("\n".join(slide_text_list))

    document.close()

    return '\n'.join(text_list)


if __name__ == '__main__':
    import sys
    result = get_pptx_text(sys.argv[1])
    print(result)