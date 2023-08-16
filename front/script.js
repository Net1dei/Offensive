async function myClick() {
  let rangeDescription = document.getElementById("out").value;
  let brand = document.querySelector(".brand").value;
  let product = document.querySelector(".product").value;
  let sostav = document.querySelector(".sostav").value;
  let category = document.querySelector(".category").value;
  let keyWords = document.querySelector(".keyWords").value;
  document.querySelector(".description").value =
    await eel.generate_descriptionJS(
      AI_value,
      category,
      product,
      brand,
      sostav,
      rangeDescription,
      keyWords
    )();
}

async function Click_gen_feedback() {
  let product = document.querySelector(".product").value;
  document.querySelector(".feedback").value = await eel.generate_feedbackJS(
    AI_value,
    product
  )();
}

let AI_value = "gpt";

function select_AI() {
  if (document.getElementById("AI_1").checked) {
    AI_value = document.getElementById("AI_1").value;
  }
  if (document.getElementById("AI_2").checked) {
    AI_value = document.getElementById("AI_2").value;
  }
}

async function getPrediction() {
  let cost = document.querySelector(".cost").value;
  let discount = document.querySelector(".discount").value;
  let rating = document.querySelector(".rating").value;
  let inStock = document.querySelector(".inStock").value;
  let Feedback = document.querySelector(".Feedback").value;
  let requestCount = document.querySelector(".requestCount").value;
  let categoryPosition = document.querySelector(".categoryPosition").value;
  document.querySelector(".prediction").value = await eel.get_predictJS(
    requestCount,
    inStock,
    Feedback,
    rating,
    cost,
    categoryPosition,
    discount
  )();
}

function clearDescription() {
  document.getElementById("description").value = "";
}
function clearFeedback() {
  document.getElementById("feedback").value = "";
}

var imgg =
  "https://w.forfun.com/fetch/ca/ca3c70c3111dde977a73ebf659a9ccc2.jpeg";
var prompt = "";
async function setImg() {
  document.querySelector(".active").setAttribute("src", imgg);
  document.getElementById("mainImage1").setAttribute("src", imgg);
  prompt = document.querySelector(".prompt").value;
}

var NomerOfImage = 0;
async function nextNomerOfImage() {
  NomerOfImage = NomerOfImage + 1;
  if (NomerOfImage === 4) {
    NomerOfImage = 0;
  }
}
async function prevNomerOfImage() {
  NomerOfImage = NomerOfImage - 1;
  if (NomerOfImage === -1) {
    NomerOfImage = 3;
  }
}
async function newimg() {
  let Imagee = localStorage.getItem("Imagee");

  if (NomerOfImage === 0) {
    document.getElementById("carouselImg0").setAttribute("src", Imagee);
    document.getElementById("galeryImg0").setAttribute("src", Imagee);
  } else if (NomerOfImage === 0) {
    document.getElementById("carouselImg0").setAttribute("src", Imagee);
    document.getElementById("galeryImg0").setAttribute("src", Imagee);
  } else if (NomerOfImage === 1) {
    document.getElementById("carouselImg1").setAttribute("src", Imagee);
    document.getElementById("galeryImg1").setAttribute("src", Imagee);
  } else if (NomerOfImage === 2) {
    document.getElementById("carouselImg2").setAttribute("src", Imagee);
    document.getElementById("galeryImg2").setAttribute("src", Imagee);
  } else if (NomerOfImage === 3) {
    document.getElementById("carouselImg3").setAttribute("src", Imagee);
    document.getElementById("galeryImg3").setAttribute("src", Imagee);
  }
}
/*async function setReGenerateImage() {
  if (NomerOfImage === 0) {
    document.getElementById("carouselImg0").setAttribute("src", "/img/0.png");
    document.getElementById("galeryImg0").setAttribute("src", "/img/0.png");
    document.getElementById("carouselImg0").setAttribute("src", "/img/0.jpg");
    document.getElementById("galeryImg0").setAttribute("src", "/img/0.jpg");
  } else if (NomerOfImage === 1) {
    document.getElementById("carouselImg1").setAttribute("src", "/img/1.png");
    document.getElementById("galeryImg1").setAttribute("src", "/img/1.png");
    document.getElementById("carouselImg1").setAttribute("src", "/img/1.jpg");
    document.getElementById("galeryImg1").setAttribute("src", "/img/1.jpg");
  } else if (NomerOfImage === 2) {
    document.getElementById("carouselImg2").setAttribute("src", "/img/2.png");
    document.getElementById("galeryImg2").setAttribute("src", "/img/2.png");
    document.getElementById("carouselImg2").setAttribute("src", "/img/2.png");
    document.getElementById("galeryImg2").setAttribute("src", "/img/2.png");
  } else if (NomerOfImage === 3) {
    document.getElementById("carouselImg3").setAttribute("src", "/img/3.png");
    document.getElementById("galeryImg3").setAttribute("src", "/img/3.png");
    document.getElementById("carouselImg3").setAttribute("src", "/img/3.png");
    document.getElementById("galeryImg3").setAttribute("src", "/img/3.png");
  }
}*/

async function analitic_top() {
  const images = [
    "/graphs/цвета.png",
    "/graphs/hist_в наличии.png",
    "/graphs/hist_длина описания.png",
    "/graphs/hist_Кол-во отзывов.png",
    "/graphs/hist_Куплено за год.png",
    "/graphs/hist_Отзывы символы.png",
    "/graphs/hist_рейтинг float.png",
    "/graphs/hist_скидка.png",
    "/graphs/hist_цена.png",
    "/graphs/hist_Число запросов в Интернете за месяц.png",
    "/graphs/hist_Число запросов в Wildberries за 3 месяца.png",
  ];
  await eel.analitic_topJS();

  const container = document.getElementById("image-container");

  for (let i = 0; i < images.length; i++) {
    const img = document.createElement("img");
    img.className = "nomberimg";
    const br = document.createElement("br");
    img.src = images[i];
    img.alt = "Нет графика";
    container.appendChild(img);
  }
}
async function analiticFromInternet() {
  let inputValue = document.querySelector(".PersonalRequestInternet").value;
  let func = await eel.get_requests_InternetJS(inputValue)();
  let nomberOfAnalitic = 0;

  // перебираем элементы массива func
  func.forEach((student) => {
    student.forEach((data) => {
      document.getElementById("analitic" + nomberOfAnalitic).value = data;
      nomberOfAnalitic = nomberOfAnalitic + 1;
    });
  });
}
async function analiticFromWB() {
  let inputValue = document.querySelector(".PersonalRequestWB").value;
  let func = await eel.get_requests_WildberriesJS(inputValue)();
  let nomberOfAnalitic = 0;

  // перебираем элементы массива func
  func.forEach((student) => {
    student.forEach((data) => {
      document.getElementById("Analitic" + nomberOfAnalitic).value = data;
      nomberOfAnalitic = nomberOfAnalitic + 1;
    });
  });
}
async function generateImg() {
  let Imagee = localStorage.getItem("Imagee");
  let Prompt = document.querySelector(".prompt").value;
  let Text = "Text";
  await eel.gen_imgJS(Imagee, Prompt, Text)();
  document.getElementById("carouselImg0").setAttribute("src", "/img/0.png");
  document.getElementById("galeryImg0").setAttribute("src", "/img/0.png");
  document.getElementById("carouselImg1").setAttribute("src", "/img/1.png");
  document.getElementById("galeryImg1").setAttribute("src", "/img/1.png");
  document.getElementById("carouselImg2").setAttribute("src", "/img/2.png");
  document.getElementById("galeryImg2").setAttribute("src", "/img/2.png");
  document.getElementById("carouselImg3").setAttribute("src", "/img/3.png");
  document.getElementById("galeryImg3").setAttribute("src", "/img/3.png");
}
function delGraphs() {
  const delImg = document.querySelectorAll(".nomberimg");
  delImg.forEach((nomberimg) => {
    nomberimg.remove();
  });
}
