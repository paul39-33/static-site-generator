from textnode import *
from htmlnode import *

def main():
    tes1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    tes2 = HTMLNode("p", "Lorem ipsum dolor sit amet consectetur adipiscing elit.", 
    props={
    "href": "https://www.google.com",
    "target": "_blank",
})
    print(f"tes1 : {tes1}")
    print(f"tes2 : {tes2}")
    print(f"tes2 props_to_html : {tes2.props_to_html()}")

main()
