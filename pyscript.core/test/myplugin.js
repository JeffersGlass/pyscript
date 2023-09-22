console.log("MY PLUGIN!")

import { hooks } from '@pyscript/core'

// From codedent
function content (t) {
    for (var s = t[0], i = 1, l = arguments.length; i < l; i++)
      s += arguments[i] + t[i];
    return s;
  }
  
  const dedent = {
    object(...args) {
      return this.string(content(...args));
    },
    string(content) {
      for (const line of content.split(/[\r\n]+/)) {
        // skip initial empty lines
        if (line.trim().length) {
          // trap indentation at the very first line of code
          if (/^(\s+)/.test(line))
            content = content.replace(new RegExp('^' + RegExp.$1, 'gm'), '');
          // no indentation? all good: get out of here!
          break;
        }
      }
      return content;
    }
  };

const codedent = (tpl, ...values) => dedent[typeof tpl](tpl, ...values);

let bgred = 0 

function pulsebackground(up=true){
  console.log("pulsebackground ", bgred)
  document.getElementById("divOutput").style.backgroundColor = `rgb(255, ${bgred}, ${bgred})`;
  bgred += up ? 5 : -5
  if (bgred >= 255 || bgred <= 0) up = !up
  setTimeout(pulsebackground, 10, up)
}

function panic(){
    panic = () => {}
    console.log("PANIC")
    const style = document.createElement('style')
    style.innerHTML = `.imgbg { display: block; width: 150px; height: 112px; background-image: url(bunny2.jpg); background-repeat: no-repeat; }
    .imgpos { position:absolute; background-position: 0px 0px; }` 
    document.head.append(style)
    const div = document.createElement('div');
    div.style.height = "100vh";
    div.style.width = "100%";
    div.style.overflow = 'auto'
    //div.style.position = "absolute"
    div.id="divOutput";
    if (document.body.firstChild) document.body.insertBefore(div, document.body.firstChild)
    else document.body.append(div)

    pulsebackground()

    var strHTML = '';
    var vtop=0;
    var vleft=0;
    for (var i = 0; i < 10; i++) 
    {
      vtop += 5;
      vleft += 5;
      strHTML += "<img src='bunny3.png' style='position:fixed; top:" + vtop + "px;left:" + vleft + "px;width:auto;height:auto;max-width:400px;display:block;scale:.25'>";
    }
    document.getElementById("divOutput").innerHTML = strHTML;
}

hooks.onInterpreterReady.add(
    function preventAwaitables(wrap, element){
        console.log("wrap:", wrap)
        //console.log("element:", element)

        const src = codedent(element.textContent)
        console.log(src)

        const module_dict = wrap.run('{}')

        const usesAwait = wrap.run(`
        import types

        import ast

        class TopLevelAwaitFinder(ast.NodeVisitor):
            def is_source_top_level_await(self, source):
                self.async_found = False
                node = ast.parse(source)
                self.generic_visit(node)
                return self.async_found

            def visit_Await(self, node):
                self.async_found = True

            def visit_AsyncFor(self, node):
                self.async_found = True

            def visit_AsyncWith(self, node):
                self.async_found = True

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
                pass  # Do not visit children of async function defs


        def uses_top_level_await(source: str) -> bool:
            return TopLevelAwaitFinder().is_source_top_level_await(source)

        uses_top_level_await
        `,  {globals: module_dict})

        if(usesAwait(src)){
            console.warn("YOU'RE ABOUT TO USE TOP LEVEL AWAIT??? NOOOOOO!!!\nvvvvv Don't do this vvvvvv\n", src)
        }
        element.textContent = ""
        panic()
    }
)

