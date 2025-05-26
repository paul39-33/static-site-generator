class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        print(f"\ntag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}")
        #raise NotImplementedError
        final_html_text =''

        if not self.tag:
            html_text = f"{self.value}"
            return html_text
    

        final_html_text += f"<{self.tag}"

        if self.props:
            props_text = ' ' + self.props_to_html()
            final_html_text += props_text

        final_html_text += ">"

        #print(f"html_text0: {final_html_text}")

        if self.children:

            for child in self.children:
                child_html_text = child.to_html()
                #print(f"child_html_text: {child_html_text}")
                final_html_text += child_html_text

        
        final_html_text += f"</{self.tag}>"
        print(f"\nFINAL HTML TEXT: {final_html_text}")
        final_html_text += "\n"    
        return final_html_text

    
    def props_to_html(self):
        dict2 = ' '.join(f'{k}="{v}"' for k, v in self.props.items())
        return dict2

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, target):
        return (self.tag == target.tag and 
        self.value == target.value and 
        self.children == target.children and 
        self.props == target.props)


class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        super().__init__(tag, value, [], props)

    #Example ('a', "Visit Boot.dev", "href": "https://boot.dev")
    def to_html(self):
        print(f"\nSELF: {self}")
        '''if not self.value:
            raise ValueError("Node needs a value")'''
        if not self.tag:
            return str(self.value)

        props_html = ""

        if self.props:
            props_html = ' ' + self.props_to_html()
        
        #Example <a href="https://boot.dev">Visit Boot.dev</a>
        if self.tag == "img":
            html_node = f"<{self.tag}{props_html}>"
        else:
            html_node = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        #print(f"=========to_html: {html_node}")
        return html_node

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        html = f"<{self.tag}>"

        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

        

            
        
        