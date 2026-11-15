const {chromium}=require('/tmp/kissari-browser-qa/node_modules/playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:'/snap/bin/chromium',headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const width of [1920,1280,960,390]){
  await page.setViewportSize({width,height:1000});
  await page.goto('http://127.0.0.1:1314/blog/');await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.blog-row').count(),5);
  for(const row of await page.locator('.blog-row').all()){
   assert.equal(await row.locator('.article-card').count(),6);
   const track=row.locator('.blog-track');
   assert(await track.evaluate(e=>e.scrollWidth>e.clientWidth));
   await row.locator('[data-next]').click();
   await page.waitForFunction(el=>el.scrollLeft>0,await track.elementHandle());
   await track.focus();await page.keyboard.press('End');
   await page.waitForFunction(el=>el.scrollWidth-el.clientWidth-el.scrollLeft<3,await track.elementHandle());
   await track.focus();await page.keyboard.press('Home');
   await page.waitForFunction(el=>el.scrollLeft<3,await track.elementHandle());
  }
  for(const id of ['actus','jusdecerveau','interviews','outils']){
   await page.locator(`[data-filter="${id}"]`).click();
   assert.equal(await page.locator('.blog-row:visible').count(),1);
   assert.equal(await page.locator('.blog-row:visible').getAttribute('data-category'),id);
  }
  await page.locator('[data-filter="all"]').click();
  assert.equal(await page.locator('.blog-row:visible').count(),5);
  const metrics=await page.evaluate(()=>({viewport:innerWidth,page:document.documentElement.scrollWidth,heights:[...document.querySelectorAll('.article-card')].slice(0,6).map(e=>Math.round(e.getBoundingClientRect().height))}));
  assert(metrics.page<=width,JSON.stringify(metrics));
  await page.locator('.blog-row').first().scrollIntoViewIfNeeded();
  await page.screenshot({path:`/mnt/datas/01-dev/web/maversionkissari/.blog-rails-${width}.png`});
  console.log(JSON.stringify(metrics));
 }
 // Zoom CSS : contrôle complémentaire de grossissement, distinct du zoom natif navigateur.
 await page.setViewportSize({width:1920,height:1200});
 for(const zoom of [1.5,2]){
  await page.goto('http://127.0.0.1:1314/blog/');
  await page.evaluate(z=>document.documentElement.style.zoom=z,zoom);
  const row=page.locator('.blog-row').first();
  await row.locator('[data-next]').click();
  assert(await row.locator('.blog-track').evaluate(e=>e.scrollLeft>0));
  await row.scrollIntoViewIfNeeded();
  await page.screenshot({path:`/mnt/datas/01-dev/web/maversionkissari/.blog-zoom-${zoom}.png`});
  console.log(`PASS grossissement CSS ${zoom}`);
 }
 assert.deepEqual(errors,[]);console.log('PASS: 5 rails, 6 cartes/rail, flèches, clavier, filtres, débordement, aucune erreur JS');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
