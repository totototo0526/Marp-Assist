module.exports = {
  apps : [{
    name   : "marp-api",
    script : "./index.js",
    cwd    : __dirname,
    watch  : false,
    env    : {
      "NODE_ENV": "production",
    }
  }]
}
