import re

import sublime
import sublime_plugin

emptyRegex = re.compile(r"^\s*$")

class SelectBlockCommand(sublime_plugin.TextCommand):
    """
        Selects a block of text bounded by an empty line,
        a line containing only whitespace, or the beginning/end of a file.
    """
    
    def run(self, edit):
        def empty(text):
            if len(text) == 0:
                return True
            
            return re.match(emptyRegex, text) != None
        
        selection = self.view.sel()
        
        if len(selection) > 1:
            return
        
        start = self.view.line(selection[0])
        
        if empty(self.view.substr(start)):
            return
        
        top = start
        bottom = start
        foundTop = False
        foundBottom = False
        
        while not foundTop or not foundBottom:
            if not foundTop:
                newTop = self.view.line(
                    self.view.line(
                        sublime.Region(top.a - 1, top.a - 1)
                    )
                )
                
                if newTop.a < 0:
                    foundTop = True
                else:
                    if empty(self.view.substr(newTop)):
                        foundTop = True
                    else:
                        top = newTop
            
            if not foundBottom:
                newBottom = self.view.line(
                        self.view.line(
                            sublime.Region(bottom.b + 1, bottom.b + 1)
                        )
                    )
                
                if newBottom.b > self.view.size():
                    foundBottom = True
                else:
                    if empty(self.view.substr(newBottom)):
                        foundBottom = True
                    else:
                        bottom = newBottom
        
        selection.clear()
        selection.add(sublime.Region(top.a, bottom.b))
