const puppeteer = require("puppeteer");
const fs = require("fs");
require("dotenv").config({ path: "../.env" });

(async function () {
	const browser = await puppeteer.launch({ headless: false });
	const page = await browser.newPage();
	await page.setViewport({
		width: 1200,
		height: 800,
	});
	await page.goto(process.env.URL_BURGER_KING);
	await something;
	await page.waitForSelector(".bk-category__item");
	const categories = await page.$$(".bk-category__item");
	const burgers = categories[1];
	await burgers.click();

	await autoScroll(page);

	const burgers_beef = await page.$$(".bk-dish-card");
	await burgers_beef[0].click();
	await page.click();

	//await burgers_beef[1].click()

	//await browser.close()
})();

async function autoScroll(page) {
	await page.evaluate(async () => {
		await new Promise((resolve, reject) => {
			var totalHeight = 0;
			var distance = 100;
			var timer = setInterval(() => {
				var scrollHeight = document.body.scrollHeight;
				window.scrollBy(0, distance);
				totalHeight += distance;

				if (totalHeight >= scrollHeight - window.innerHeight) {
					clearInterval(timer);
					resolve();
				}
			}, 100);
		});
	});
}
