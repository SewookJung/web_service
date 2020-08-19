const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const mnfactureBox = document.getElementById("mnfacture");

const getListsProductModel = (param) => {
  $.ajax({
    url: "/equipment/stock/get/list/",
    data: param,
    type: "POST",
    dataType: "json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      const stockInfoDiv = document.getElementById("body__stock-info");
      stockInfoDiv.innerHTML = "";
      const h6 = document.createElement("h6");

      const stocksData = data.stocks;
      const mnfactureName = Object.keys(stocksData[0])[0];
      const stockList = Object.values(stocksData[0][mnfactureName]);

      h6.classList.add("text-muted");
      h6.innerText = mnfactureName;

      for (let i = 0; i < stockList.length; i++) {
        const modelName = Object.keys(stockList[i])[0];
        const productName = Object.values(stockList[i])[0].product;
        const keepCount = Object.values(stockList[i])[0].keep;
        const soldCount = Object.values(stockList[i])[0].sold;
        const disposalCount = Object.values(stockList[i])[0].disposal;
        const returnCount = Object.values(stockList[i])[0].return;
        const productId = Object.values(stockList[i])[0].id;

        const cardDiv = document.createElement("div");
        const cardBodyDiv = document.createElement("div");
        const stockModelNameDiv = document.createElement("div");
        const stockProductNameDiv = document.createElement("div");
        const stockStatusListsDiv = document.createElement("div");

        const stockKeepDiv = document.createElement("div");
        const stockKeepTitleDiv = document.createElement("div");
        const stockKeepCountDiv = document.createElement("div");
        const stockSoldDiv = document.createElement("div");
        const stockSoldTitleDiv = document.createElement("div");
        const stockSoldCountDiv = document.createElement("div");
        const stockDisposalDiv = document.createElement("div");
        const stockDisposalTitleDiv = document.createElement("div");
        const stockDisposalCountDiv = document.createElement("div");
        const stockReturnDiv = document.createElement("div");
        const stockReturnTitleDiv = document.createElement("div");
        const stockReturnCountDiv = document.createElement("div");

        stockKeepTitleDiv.innerText = "재 고";
        stockKeepCountDiv.innerText = keepCount;
        stockKeepCountDiv.setAttribute(
          "onclick",
          `goToDetailPage(event, ${productId}, 'keep')`
        );
        stockKeepCountDiv.style.cursor = "pointer";
        stockKeepDiv.id = "stock-status";
        stockKeepDiv.classList.add("stock-status__keep");
        stockKeepDiv.append(stockKeepTitleDiv);
        stockKeepDiv.append(stockKeepCountDiv);

        stockSoldTitleDiv.innerText = "납 품";
        stockSoldCountDiv.innerText = soldCount;
        stockSoldCountDiv.setAttribute(
          "onclick",
          `goToDetailPage(event, ${productId}, 'sold')`
        );
        stockSoldCountDiv.style.cursor = "pointer";
        stockSoldDiv.id = "stock-status";
        stockSoldDiv.classList.add("stock-status__sold");
        stockSoldDiv.append(stockSoldTitleDiv);
        stockSoldDiv.append(stockSoldCountDiv);

        stockDisposalTitleDiv.innerText = "폐 기";
        stockDisposalCountDiv.innerText = disposalCount;
        stockDisposalCountDiv.setAttribute(
          "onclick",
          `goToDetailPage(event, ${productId}, 'disposal')`
        );
        stockDisposalCountDiv.style.cursor = "pointer";
        stockDisposalDiv.id = "stock-status";
        stockDisposalDiv.classList.add("stock-status__disposal");
        stockDisposalDiv.append(stockDisposalTitleDiv);
        stockDisposalDiv.append(stockDisposalCountDiv);

        stockReturnTitleDiv.innerText = "반 납";
        stockReturnCountDiv.innerText = returnCount;
        stockReturnCountDiv.setAttribute(
          "onclick",
          `goToDetailPage(event, ${productId}, 'return')`
        );
        stockReturnCountDiv.style.cursor = "pointer";
        stockReturnDiv.id = "stock-status";
        stockReturnDiv.classList.add("stock-status__return");
        stockReturnDiv.append(stockReturnTitleDiv);
        stockReturnDiv.append(stockReturnCountDiv);

        stockStatusListsDiv.append(stockKeepDiv);
        stockStatusListsDiv.append(stockSoldDiv);
        stockStatusListsDiv.append(stockReturnDiv);
        stockStatusListsDiv.append(stockDisposalDiv);

        cardDiv.append(cardBodyDiv);
        cardBodyDiv.append(stockModelNameDiv);
        cardBodyDiv.append(stockStatusListsDiv);
        stockModelNameDiv.innerText = modelName;
        stockProductNameDiv.innerText = productName;
        stockModelNameDiv.append(stockProductNameDiv);

        cardDiv.classList.add("card");
        cardBodyDiv.classList.add("card-body", "stock-lists");
        stockModelNameDiv.classList.add("stock-model");
        stockStatusListsDiv.classList.add("stock-status-lists");
        stockProductNameDiv.classList.add("stock-product-name");
        stockInfoDiv.append(cardDiv);
      }
    },
    error: function (request, status, error) {
      console.log(request);
      const errorMsg = JSON.parse(request.responseText).msg;
      alert(errorMsg);
    },
  });
};

mnfactureBox.addEventListener("change", (event) => {
  const mnfactureId = event.target.value;
  if (!mnfactureId == "") {
    param = {};
    param.mnfactureId = mnfactureId;
    getListsProductModel(param);
  }
});

const goToDetailPage = (event, productId, status) => {
  const selectedStockCount = Number(event.target.innerText);
  if (selectedStockCount < 1) alert("선택한 목록이 존재하지 않습니다.");
  else window.location = `/equipment/stock/${productId}/${status}`;
};

$(document).ready(function () {
  const coreEdgeId = 4;
  const defaultMnfactureId = coreEdgeId;
  $("select[name=mnfacture]").val(defaultMnfactureId);
  $(".selectpicker").selectpicker("refresh");
  param = {};
  param.mnfactureId = defaultMnfactureId;
  getListsProductModel(param);
});
