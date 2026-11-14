/* Independent geometry checks and a browser check of the exported teaching model.
   Usage: node verify-contact.cjs [path-to-playwright] [browser-executable]
   Omit both arguments to run the geometry checks without opening a browser. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const source = fs.readFileSync(path.join(__dirname,'unit-distance-contact.fragment.html'),'utf8');
const script = source.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const body = script.slice(script.indexOf('function geometry('),script.indexOf('function render()'));
const box = {Math};
vm.createContext(box);
vm.runInContext('const a=-0.6,b=0.6,tolerance=1e-9;'+body+';this.geometry=geometry;',box);
const close = (x,y)=>Math.abs(x-y)<1e-10;
const cases = [
  {p:[.65,.7],min:Math.sqrt(.4925),max:Math.sqrt(2.0525),contacts:1,strict:true},
  {p:[0,.2],min:.2,max:Math.sqrt(.4),contacts:0,strict:false},
  {p:[0,1.3],min:1.3,max:Math.sqrt(2.05),contacts:0,strict:false},
  {p:[0,.9],min:.9,max:Math.sqrt(1.17),contacts:2,strict:true},
  {p:[0,1],min:1,max:Math.sqrt(1.36),contacts:1,strict:false}
];
for (const c of cases) {
  const g = box.geometry(...c.p);
  assert(close(g.minimum,c.min)&&close(g.maximum,c.max));
  assert.equal(g.contacts.length,c.contacts);
  assert.equal(g.strict,c.strict);
  for (const q of g.contacts) assert(close(Math.hypot(c.p[0]-q,c.p[1]),1));
}
let samples = 0;
for (let ix=-150;ix<=150;ix+=3) for(let iy=-150;iy<=150;iy+=3) {
  const x=ix/100,y=iy/100,g=box.geometry(x,y);
  // Independent capsule criterion: rectangle strip OR an endpoint disk.
  const insideCapsule=(Math.abs(x)<=.6&&Math.abs(y)<1)||Math.hypot(x+.6,y)<1||Math.hypot(x-.6,y)<1;
  const outsideLens=Math.hypot(x+.6,y)>1 || Math.hypot(x-.6,y)>1;
  if(Math.abs(g.minimum-1)>1e-8&&Math.abs(g.maximum-1)>1e-8) assert.equal(g.strict,insideCapsule&&outsideLens);
  if(g.strict) assert(g.contacts.length>0);
  for(const q of g.contacts) assert(close(Math.hypot(x-q,y),1));
  samples++;
}
async function main() {
  const result={geometry:'passed',examples:cases.length,gridSamples:samples,javascriptSyntax:'passed',browser:'not run'};
  if(process.argv[2]) {
    const {chromium}=require(process.argv[2]);
    const browser=await chromium.launch({headless:true,executablePath:process.argv[3]});
    try {
      const page=await browser.newPage({viewport:{width:800,height:800}});
      const errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto(pathToFileURL(path.join(__dirname,'unit-distance-contact.html')).href);
      const frame=page.frameLocator('iframe');
      await frame.locator('#mathathon-contact').waitFor();
      await frame.getByRole('button',{name:'Middle matters',exact:true}).click();
      assert.match(await frame.locator('#contact-result').textContent(),/Minimum 0\.900.*Maximum 1\.082.*Contact forced/);
      assert.equal(await frame.locator('.contact-witness').count(),2);
      await frame.getByRole('button',{name:'All farther',exact:true}).click();
      assert.match(await frame.locator('#contact-result').textContent(),/No unit-distance contact/);
      assert.equal(await frame.locator('.contact-witness').count(),0);
      await frame.getByRole('button',{name:'Straddles 1',exact:true}).click();
      const qa=path.resolve(__dirname,'../../..','.scratch/exposition-qa');
      fs.mkdirSync(qa,{recursive:true});
      await page.screenshot({path:path.join(qa,'contact-desktop.png'),fullPage:true});
      await page.setViewportSize({width:360,height:850});
      await frame.getByRole('button',{name:'Middle matters',exact:true}).click();
      const bounds=await frame.locator('#mathathon-contact').evaluate(el=>({width:el.clientWidth,scroll:el.scrollWidth}));
      assert(bounds.scroll<=bounds.width+1,'mobile horizontal overflow');
      await page.screenshot({path:path.join(qa,'contact-mobile.png'),fullPage:true});
      assert.deepEqual(errors,[]);
      result.browser='passed';
      result.browserChecks=['selected preset controls','contact markers','mobile width','no page errors'];
    } finally {await browser.close();}
  }
  console.log(JSON.stringify(result,null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
