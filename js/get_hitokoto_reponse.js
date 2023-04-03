async function getData() {
   try {
    const response = await fetch('https://v1.hitokoto.cn');
    const data = await response.json();
    return data;
  } catch (error) {
    return error
  }
}

getData().then(data => console.log(data));