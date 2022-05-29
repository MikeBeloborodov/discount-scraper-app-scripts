const puppeteer = require('puppeteer');
const fs = require('fs');
require('dotenv').config({path: '../../.env'});

(async function(){
    const browser = await puppeteer.launch({headless: true})
    const page = await browser.newPage();
    await page.setViewport({
        width: 1200,
        height: 800
    })
    await page.goto(process.env.URL_SUSHI_DOMA)

    await page.waitForSelector('.product-card')
    // await page.screenshot({path: "screenshot.png"})

    await autoScroll(page);

    page_html = await page.content(); 
    fs.writeFile(`../html/${process.env.FILE_NAME_SUSHI_DOMA}.html`, page_html, function (err) {
        if (err) return console.log(err);
      })

    await browser.close()
})();

async function autoScroll(page){
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight - window.innerHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}