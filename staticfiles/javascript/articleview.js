    Pagination();

    function Pagination() {
        var mainHeading = document.getElementById("mainHeading");
        var mainHeadingText = mainHeading.innerHTML;

        var sideNavUL = document.getElementById("sideNavUL");
        var li = sideNavUL.getElementsByTagName("li");

        for (i = 0; i < li.length; i++) {
            var mainHeadingmatch = li[i].getElementsByClassName("a")[0];
            var mainHeadingMatch = mainHeadingmatch.innerHTML;

            if (mainHeadingText === mainHeadingMatch) {
                li[i].style.backgroundColor = "#1496f4";
                mainHeadingmatch.style.color = "white";
            } else {
                li[i].style.backgroundColor = "";
            }

        }
    }

    copyRightDate(2020)

    function copyRightDate(x) {
        var d = new Date;
        var year = d.getFullYear();
        var footerDate = document.getElementById("footerdate");
        if (year == x) {
            footerDate.innerHTML = year;
        } else {
            footerDate.innerHTML = x + "-" +
                year;
        }
    }

    checkSideNav();

    function checkSideNav() {
        var sideNav = document.getElementById("sideNav");
        var closeButton = document.getElementById("close");
        var toggle = document.getElementById("toggle")
        var x_axis = window.innerWidth;

        if (x_axis <= 999) {
            sideNav.style.display = "none";
            closeButton.style.display = "block";
            toggle.style.display = "block"
        } else {
            if (x_axis >= 999) {
                closeButton.style.display = "none"
                sideNav.style.display = "block";
                toggle.style.display = "none"
            }
        }
    }

    function SearchFunction() {
        var input, filter, sideNavUL, li, contents, i;
        input = document.getElementById("SearchInput");
        filter = input.value.toUpperCase();
        sideNavUL = document.getElementById("sideNavUL");
        li = sideNavUL.getElementsByTagName("li");
        for (i = 0; i < li.length; i++) {
            contents = li[i].getElementsByTagName("a")[0];
            if (contents.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "block";
            } else {
                li[i].style.display = "none";

            }
        }
    }

    function show() {
        var sideNav = document.getElementById("sideNav");
        if (sideNav.style.display === "none") {
            sideNav.style.display = "block";
            var closeButton = document.getElementById("close");
            closeButton.style.display = "block";
        } else {
            showNot();
        };

    };

    function showNot() {
        var sideNav = document.getElementById("sideNav");
        sideNav.style.display = "none";
        var closeButton = document.getElementById("close");
        closeButton.style.display = "none";

    }

    document.getElementsByTagName("BODY")[0].onresize = function() {
        myResize()
    };

    function myResize() {
        var closeButton = document.getElementById("close");
        var sideNav = document.getElementById("sideNav");
        var x_axis = window.innerWidth;
        var fixing = document.getElementById("fixing");
        var fixing2 = document.querySelector(".fixing")
        if (x_axis >= 999) {
            sideNav.removeAttribute("style");
            closeButton.style.display = "none";
            stickSideBar();
        }
        if (x_axis <= 999) {
            fixing.removeAttribute("style");
            fixing2.removeAttribute("style")
            sideNav.removeAttribute("style");
        } else {
            displayHead();

        }
        checkSideNav()
    }

    document.getElementsByTagName("BODY")[0].onscroll = function() {
        displayHead(), backToTop(), stickSideBar()
    };

    function displayHead() {
        var bannerParagraph = document.getElementById("bannerParagraph");
        var bannerParagraphOffSet = bannerParagraph.offsetTop;
        var fixing = document.getElementById("fixing");
        var fixing2 = document.querySelector(".fixing")
        var desktopView = 1000;
        var x_axis = window.innerWidth;
        var y_axis = window.pageYOffset ||
            document.documentElement.scrollTop ||
            document.body.scrollTop;
        if (x_axis >= desktopView && y_axis >= bannerParagraphOffSet) {
            fixing.style.display = "block"
            fixing2.style.display = "none"
        } else if (x_axis >= desktopView && y_axis <= bannerParagraphOffSet) {
            fixing.style.display = "none"
            fixing2.style.display = "block"
        }
    }

    function backToTop() {
        var y_axis_offset = window.pageYOffset ||
            document.documentElement.scrollTop ||
            document.body.scrollTop;
        x = "1500";
        var backToTopButton = document.getElementById("backToTop");
        if (y_axis_offset >= x) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    }

    function stickSideBar() {
        var x_axis = window.innerWidth;
        var y_axis = window.pageYOffset ||
            document.documentElement.scrollTop ||
            document.body.scrollTop;
        var desktopView = 1000
        var sideNav = document.getElementById("sideNav");
        var main = document.getElementById("main");

        if (x_axis >= desktopView && y_axis >= 340) {
            sideNav.style.position = "fixed";
            sideNav.style.height = "85%";
            sideNav.style.top = "98px"
            main.style.left = "25%"
        } else if (x_axis >= desktopView && y_axis <= 390) {
            sideNav.style.position = "relative"
            sideNav.style.height = "750px";
            sideNav.style.top = "0px"
            main.style.left = "0%"
        }
        if (x_axis <= 999) {
            sideNav.style.top = "100px";
        }
    }
    //for Safari and his brothers
    window.addEventListener('scroll', function() {
        displayHeadSafari(), backToTop(), stickSideBarSafari()
    });
    window.addEventListener('resize', function() {
        myResizeSafari()
    });
    var SafariDetector = !/function/.test(window.HTMLElement)

    checkSideNavSafari();

    function checkSideNavSafari() {
        var sideNav = document.getElementById("sideNav");
        var x_axis = document.documentElement.clientWidth ||
            document.body.clientWidth;
        var closeButton = document.getElementById("close");
        var toggle = document.getElementById("toggle")
        if (x_axis <= 999 && SafariDetector) {
            sideNav.style.display = "none";
            closeButton.style.display = "block";
            toggle.style.display = "block"
        } else {
            if (x_axis >= 999 && SafariDetector) {
                closeButton.style.display = "none"
                sideNav.style.display = "block";
                toggle.style.display = "none"
            }
        }
    }


    function myResizeSafari() {
        var closeButton = document.getElementById("close");
        var sideNav = document.getElementById("sideNav");
        var x_axis = document.documentElement.clientWidth ||
            document.body.clientWidth;
        var desktopView = 999
        var fixing = document.getElementById("fixing");
        var fixing2 = document.querySelector(".fixing")
        if (x_axis >= desktopView && SafariDetector) {
            sideNav.removeAttribute("style");
            closeButton.style.display = "none";
            stickSideBarSafari();
            sideNav.style.display = "block";
            sideNav.style.position = "relative";
        }
        if (x_axis <= desktopView && SafariDetector) {
            fixing.removeAttribute("style");
            fixing2.removeAttribute("style")
            sideNav.removeAttribute("style");
            sideNav.style.position = "fixed";
        } else {
            displayHead();
        }
        checkSideNavSafari()
    }

    function displayHeadSafari() {
        var bannerParagraph = document.getElementById("bannerParagraph");
        var bannerParagraphOffSet = bannerParagraph.offsetTop;
        var desktopView = 1000
        var fixing = document.getElementById("fixing");
        var fixing2 = document.querySelector(".fixing")
        var x_axis = document.documentElement.clientWidth ||
            document.body.clientWidth;
        var y_axis_offset = window.pageYOffset ||
            document.documentElement.scrollTop ||
            document.body.scrollTop;
        if (x_axis >= desktopView && y_axis_offset >= bannerParagraphOffSet && SafariDetector) {
            fixing.style.display = "block"
            fixing2.style.display = "none"
        } else if (x_axis >= desktopView && y_axis_offset <= bannerParagraphOffSet && SafariDetector) {
            fixing.style.display = "none"
            fixing2.style.display = "block"
        }
    }

    function stickSideBarSafari() {
        var x_axis = document.documentElement.clientWidth ||
            document.body.clientWidth;
        var y_axis_offset = window.pageYOffset ||
            document.documentElement.scrollTop ||
            document.body.scrollTop;
        var desktopView = 1000
        var sideNav = document.getElementById("sideNav");
        var main = document.getElementById("main");
        if (x_axis >= desktopView && y_axis_offset >= 340 && SafariDetector) {
            sideNav.style.position = "fixed";
            sideNav.style.height = "85%";
            sideNav.style.top = "98px"
            main.style.left = "25%"
        } else {
            if (x_axis >= desktopView && y_axis_offset <= 390 && SafariDetector) {
                sideNav.style.position = "relative"
                sideNav.style.height = "750px";
                sideNav.style.top = "0px"
                main.style.left = "0%"
            }
        }
        if (x_axis <= 999 && SafariDetector) {
            sideNav.style.top = "100px";
        }
    }

    var contactInputs = document.querySelectorAll(".contactInput")
    let errorMessages = {
        "full_name": "Only alphabets are allowed",
        "email": "Invalid email",
        "message": "Character not allowed",
        "subject": "Character not allowed",
        "phone_number": "Invalid phone number"
    }

    let errorTest = {
        "full_name": /[^a-z\s]/i,
        "email": /^[a-z]+\d*[a-z]*@[a-z]+\.\w+\s*$/gi,
        "message": /[^a-z\s.,;':)(0-9"#_-]/i,
        "subject": /[^a-z\s.,;':)(0-9"#_-]/i,
        "phone_number": /[^0-9+\s]/i
    }

    for (const contactInput of contactInputs) {
        contactInput.addEventListener("keyup", function() {
            let fieldName = contactInput.name;
            let fieldValue = contactInput.value;
            let fieldLength = fieldValue.length
            let selector = `${fieldName}er`;
            let errP = document.querySelector(`#${selector}`);
            if (errorTest[fieldName].test(fieldValue)) {
                errP.innerHTML = errorMessages[fieldName];
                contactInput.style.marginBottom = "0px";
            } else if (fieldName == "phone_number" && fieldLength < 11) {
                errP.innerHTML = errorMessages[fieldName];
                contactInput.style.marginBottom = "0px";

            } else if (fieldName == "email" && !errorTest[fieldName].test(fieldValue)) {
                errP.innerHTML = errorMessages[fieldName];
                contactInput.style.marginBottom = "0px";

            } else {
                errP.innerHTML = "";
                contactInput.style.marginBottom = "15px";
            }

            if (fieldValue.length == 0) {
                errP.innerHTML = "";
                contactInput.style.marginBottom = "15px";
            }

            enableSubmitButton();

        })

    }

    function enableSubmitButton() {
        let submitbtn = document.getElementById("submit");
        for (const contactInput of contactInputs) {
            let fieldName = contactInput.name;
            let fieldLength = contactInput.value.length
            let selector = `${fieldName}er`;
            let errP = document.querySelector(`#${selector}`);
            if (fieldLength <= 0) {
                console.log("no")
                submitbtn.disabled = true
                submitbtn.style.backgroundColor = "gray";
                break;
            } else if (errP.innerHTML.length > 0) {
                console.log("no")
                submitbtn.disabled = true
                submitbtn.style.backgroundColor = "gray";
                break;
            } else {
                console.log("hello")
                submitbtn.disabled = false;
                submitbtn.style.backgroundColor = "#09794a";
            }

        }

    }