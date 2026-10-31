const fs=require('fs');fs.mkdirSync('public/vendor',{recursive:true});fs.copyFileSync('node_modules/@google/model-viewer/dist/model-viewer.min.js','public/vendor/model-viewer.min.js');
