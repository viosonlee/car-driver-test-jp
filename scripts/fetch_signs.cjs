const fs = require('fs');
const path = require('path');
const https = require('https');

const signsDir = path.join(__dirname, '../public/signs');
if (!fs.existsSync(signsDir)) {
  fs.mkdirSync(signsDir, { recursive: true });
}

// Map of common traffic signs and their Wikimedia SVG URLs
const signs = [
  { id: 'stop', url: 'https://upload.wikimedia.org/wikipedia/commons/4/41/Japan_road_sign_330.svg' }, // 止まれ
  { id: 'no_entry', url: 'https://upload.wikimedia.org/wikipedia/commons/e/ec/Japan_road_sign_303.svg' }, // 進入禁止
  { id: 'one_way', url: 'https://upload.wikimedia.org/wikipedia/commons/8/87/Japan_road_sign_326-A.svg' }, // 一方通行
  { id: 'speed_limit_50', url: 'https://upload.wikimedia.org/wikipedia/commons/2/23/Japan_road_sign_323-50.svg' }, // 最高速度 50
  { id: 'no_parking', url: 'https://upload.wikimedia.org/wikipedia/commons/8/88/Japan_road_sign_316.svg' }, // 駐車禁止
  { id: 'no_stopping', url: 'https://upload.wikimedia.org/wikipedia/commons/6/64/Japan_road_sign_315.svg' }, // 駐停車禁止
  { id: 'pedestrian_crossing', url: 'https://upload.wikimedia.org/wikipedia/commons/8/80/Japan_road_sign_407-A.svg' }, // 横断歩道
  { id: 'road_closed', url: 'https://upload.wikimedia.org/wikipedia/commons/4/41/Japan_road_sign_301.svg' }, // 通行止め
  { id: 'no_u_turn', url: 'https://upload.wikimedia.org/wikipedia/commons/c/c5/Japan_road_sign_312.svg' }, // 転回禁止
  { id: 'bicycle_crossing', url: 'https://upload.wikimedia.org/wikipedia/commons/e/e0/Japan_road_sign_407-B.svg' }, // 自転車横断帯
];

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close(resolve);
      });
    }).on('error', (err) => {
      fs.unlink(dest, () => {});
      reject(err);
    });
  });
}

async function main() {
  for (const sign of signs) {
    const dest = path.join(signsDir, `${sign.id}.svg`);
    console.log(`Downloading ${sign.id}.svg...`);
    try {
      await download(sign.url, dest);
      console.log(`Saved ${sign.id}.svg`);
    } catch (e) {
      console.error(`Failed to download ${sign.id}`, e);
    }
  }
}

main();
