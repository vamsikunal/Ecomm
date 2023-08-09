var localityElement = document.getElementById('locality');
var districtElement = document.getElementById('district');
var stateElement = document.getElementById('state');

function getPin() {
  let val = document.getElementById('pincode').value;
  getName(val);
}

function removePin() {
 localityElement.innerHTML = "";
 districtElement.value = "";
 stateElement.value = "";
}

async function getName(pincode) {
  let api_url = 'https://api.postalpincode.in/pincode/'+pincode;
  const responce = await fetch(api_url);
  const data = await responce.json();
  info = data[0].PostOffice;
  for (let i = 0; i < info.length; i++) {
  var option = document.createElement("option");
  option.text = info[i].Name;
  option.value = info[i].Name;
  localityElement.add(option);
  }
  districtElement.value = info[0].District;
  stateElement.value = info[0].State;
}
