const lowerCase = string => string
    .replace(/([a-z])([A-Z])/g, "$1-$2")
    .replace(/[\s_]+/g, '-')
    .replace(/[,]+/g, '')
    .toLowerCase();

locations = document.getElementsByTagName("button");

for (var i = 0; i < locations.length; i++) {
    elem = locations[i];
    elem.id = `${lowerCase(elem.innerHTML)}`;
}

const toggleLocation = ev => {
    const elem = ev.currentTarget;
    const main = document.getElementById("posts");
    const posts = document.getElementsByClassName("card");
    console.log(elem.innerHTML);
    if (elem.getAttribute('toggle') === 'false') {
        if (main.getAttribute('filter') === 'off') {
            setLocation(elem, main, posts);
        }
    } else {
        unsetLocation(elem, main, posts);
    }
};

const setLocation = (elem, main, posts) => {
    elem.style.fontWeight = 'bold';
    elem.setAttribute('toggle', 'true');
    main.setAttribute('filter', 'on');
    for (const post of posts) {
        if (elem.innerHTML != post.querySelector(".location").innerHTML) {
            post.style.display = "none";
        }
    }
}

const unsetLocation = (elem, main, posts) => {
    elem.style.fontWeight = 'normal';
    elem.setAttribute('toggle', 'false');
    main.setAttribute('filter', 'off');
    for (const post of posts) {
        post.style.display = "";
    }
}
