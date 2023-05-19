// querySelector setting
function $$(element) {
  return document.querySelector(element);
}
function $$all(element) {
  return document.querySelectorAll(element);
}

// 顯示等待頁面
function showLoadingPage() {
  console.log("等待中...");
  // 顯示等待頁面的內容
}
function hideLoadingPage(imageData) {
  console.log("隱藏等待頁面");
  // 顯示結果頁面的內容，使用回傳的圖片資料
}
// 顯示結果頁面
function showResultPage(imageData) {
  console.log("顯示結果頁面");
  // 顯示結果頁面的內容，使用回傳的圖片資料
}