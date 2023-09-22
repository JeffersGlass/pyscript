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
  document.getElementById("divOutput").style.backgroundColor = `rgb(255, ${bgred}, ${bgred})`;
  bgred += up ? 5 : -5
  if (bgred >= 255 || bgred <= 0) up = !up
  setTimeout(pulsebackground, 30, up)
}

const maxbuns = 10;
const bun_dims = {x: 200, y:350}


function runbuns(bunnies, lead_bun, index = 0, zindex = 0){
  lead_bun.x += lead_bun.x_speed
  if (lead_bun.x < 0 | (lead_bun.x + bun_dims.x > window.innerWidth)) {console.log("x bounce"); lead_bun.x_speed *= -1;}

  lead_bun.y += lead_bun.y_speed
  lead_bun.y_speed += 1;
  if (lead_bun.y < 0 | lead_bun.y + bun_dims.y > window.innerHeight) {
    console.log("y bounce");
    lead_bun.y_speed *= -1;
    if (lead_bun.y_speed < 0) lead_bun.y_speed *= .95
  }

  zindex += 1;

  if (bunnies.length < maxbuns){
    const img = document.createElement('img')
    img.src='bunny3.png'
    img.style=`position:fixed; top:${lead_bun.y}px;left:${lead_bun.x}px;width:auto;height:auto;max-width:400px;display:block;scale:.15'>"`
    img.style.zIndex = zindex;
    bunnies.push(img)
    document.getElementById("divOutput").appendChild(img)
  }
  else{
    bunnies[index].style.top = lead_bun.y + "px"
    bunnies[index].style.left = lead_bun.x + "px"
    bunnies[index].style.zIndex = zindex
  }

  index = (index + 1) % maxbuns;
  
  setTimeout(runbuns, 50, bunnies, lead_bun, index, zindex);
}

function panic(){
    panic = () => {}
    console.log("PANIC")
    const style = document.createElement('style')
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

    for (let i = 0; i < 5; i++){
      runbuns([], {x: Math.round(Math.random()*700+20), y: Math.round(Math.random()*100+20), x_speed: (Math.random() > .5 ? 1 : -1) * (Math.random()*15+5), y_speed:0})
    }
   
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
            panic()
            element.textContent = ""
        }
        
        
    }
)

