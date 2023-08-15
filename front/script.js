
async function myClick() {
  let rangeDescription = document.getElementById("out").value
  let brand = document.querySelector(".brand").value;
  let product = document.querySelector(".product").value;
  let sostav = document.querySelector(".sostav").value;
  let category = document.querySelector(".category").value;
  let keyWords = document.querySelector(".keyWords").value;
  document.querySelector(".description").value = await eel.generate_descriptionJS(AI_value,category,product,brand,sostav,rangeDescription,keyWords)();
  }


async function Click_gen_feedback() {
  let product = document.querySelector(".product").value;
  document.querySelector(".feedback").value = await eel.generate_feedbackJS(AI_value,product)();
  }


let AI_value = "";

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
  document.querySelector(".prediction").value = await eel.get_predictJS(requestCount,inStock,Feedback,rating,cost,categoryPosition,discount)();
  }

function clearDescription() {
  document.getElementById("description").value = "";
  }
function clearFeedback() {
  document.getElementById("feedback").value = "";
  }

async function setImg(){
  let prompt = document.querySelector(".prompt").value;
  let url = await eel.downloadurlJS(prompt)
  document.getElementById("mainImage").setAttribute("src", url);
  document.getElementById("mainImage1").setAttribute("src", url);
  }