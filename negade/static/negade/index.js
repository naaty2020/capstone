var ads = new Array();
ads[0] = "/image-photo/digital-marketing-media-website-ad-600w-1171378096.jpg";
ads[1] = "/image-vector/online-advertising-laptop-mobile-gadget-600w-634572878.jpg";
ads[2] = "/image-photo/marketing-commercial-advertising-plan-concept-600w-548073523.jpg";
ads[3] = "/image-photo/businessman-building-advertising-concept-wooden-260nw-457521961.jpg";
ads[4] = "/image-vector/business-magazine-brochure-layout-easy-600w-1700113678.jpg";
ads[5] = "/image-photo/top-view-shot-group-creative-260nw-665740429.jpg";
ads[6] = "/image-photo/advertise-advertising-advertisement-branding-concept-260nw-281221427.jpg";
ads[7] = "/image-photo/omg-concept-stupefied-dark-skinned-600w-1154675947.jpg";
ads[8] = "/image-vector/fitness-club-ads-healthy-woman-260nw-1193090389.jpg";
ads[9] = "/image-vector/cool-soft-drink-ad-ice-260nw-1109726231.jpg";

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#search').onclick = () => {
        return empty();
    };
    document.querySelectorAll('.item-out').forEach(item => {
        item.onclick = () => {
            fetch(`../item-json/${item.dataset.id}`)
                .then(response => response.json())
                .then(itm => post_item(itm));
        };
    });
    if (window.location.pathname.split("/").pop() == 'add-item' ||
            window.location.pathname.split("/").slice(-2)[0] == 'edit-item') {
        document.querySelector('#img_url').addEventListener("focusout", e => {
            preview(document.querySelector('#preview'), e.target.value);
        });
    }    
    else if (window.location.pathname.split("/").slice(-2)[0] == 'edit-page') {
        document.querySelector('#logo').addEventListener("focusout", e =>
            preview(document.querySelector('#logo-pre'), e.target.value));
        document.querySelector('#cover').addEventListener("focusout", e =>
            preview(document.querySelector('#cover-pre'), e.target.value));
    }
    else if (window.location.pathname.split("/").pop() == 'vendors') {
        document.querySelector('#filter').onclick = () => {
            if (document.querySelector('#filter-con').style.display == 'block')
                document.querySelector('#filter-con').style.display = 'none';
            else document.querySelector('#filter-con').style.display = 'block';
        };
        document.querySelector('#filter-list').querySelectorAll('li').forEach(e => {
            e.onclick = ev => {
                fetch(`type-vendor/${ev.target.dataset.name}`)
                    .then(response => response.json())
                    .then(vendors => put_vendors(vendors, ev.target.dataset.name));
            };
        });
        document.querySelector('#filter-list1').querySelectorAll('li').forEach(e => {
            e.onclick = ev => {
                v = 'Verified';
                if (parseInt(ev.target.dataset.verified) == 1) v = 'Unverified'
                fetch(`verified/${parseInt(ev.target.dataset.verified)}`)
                    .then(response => response.json())
                    .then(vendors => put_vendors(vendors, v));
            };
        });
        document.querySelector('#filter-list2').querySelectorAll('li').forEach(e => {
            e.onclick = ev => {
                v = 'Subscribed';
                if (parseInt(ev.target.dataset.sub) == 1) v = 'Unsubscribed'
                fetch(`subscribed/${parseInt(ev.target.dataset.sub)}`)
                    .then(response => response.json())
                    .then(vendors => put_vendors(vendors, v));
            };
        });
    }
    else if (window.location.pathname.split("/").pop() == '') {
        document.querySelector('#trending').onclick = e => {
            chooseBtn(e.target);
            fetch('trending-items')
                .then(response => response.json())
                .then(items => post_items(items));
        };
        document.querySelector('#new').onclick = e => {
            chooseBtn(e.target);
            fetch('new-items')
                .then(response => response.json())
                .then(items => post_items(items));
        };
        document.querySelector('#all').onclick = e => {
            chooseBtn(e.target);
            fetch('all-items')
                .then(response => response.json())
                .then(items => post_items(items));
        };
        document.querySelector('#upcoming').onclick = e => {
            chooseBtn(e.target);
            fetch('upcoming-items')
                .then(response => response.json())
                .then(items => post_items(items));
        };
        document.querySelector('#sub').onclick = e => {
            chooseBtn(e.target);
            fetch('subscription-items')
                .then(response => response.json())
                .then(items => post_items(items));
        };
    }
    if (document.querySelector('#subscribe') != null) {
        document.querySelector('#subscribe').onclick = e => {
            fetch('../subscribtion', {
                method: 'POST',
                body: JSON.stringify({ vendor_id: e.target.dataset.id })
            });
            if (e.target.innerHTML == 'Subscribed!') {
                e.target.innerHTML = 'Subscribe';
                e.target.className = 'btn btn-warning mt-4';
            }
            else {
                e.target.innerHTML = 'Subscribed!';
                e.target.className = 'btn btn-outline-secondary mt-4';
            }
        };
    }
    randomads();
});

function preview(con, e) {
    const img = document.createElement('img');
    img.src = e;
    img.className = 'img-fluid mt-3';
    con.innerHTML = '';
    con.append(img);
}

function put_vendors(vendors, typ = null) {
    document.querySelector('#ven-ul').innerHTML = '';
    vendors.forEach(v => {
        const li = document.createElement('li');
        const col = document.createElement('div');
        const col1 = document.createElement('div');
        const row = document.createElement('div');
        const a = document.createElement('a');
        const a1 = document.createElement('a');
        const img = document.createElement('img');
        li.className = 'list-group-item';
        row.className = 'row';
        col.className = 'border col-sm-3';
        col.id = 'vend-parent';
        a.href = `vendor/${v.id}`;
        a.style.height = 'inherit';
        a.style.color = 'black';
        img.src = v.logo;
        img.className = 'img-fluid';
        img.id = 'vend-logo';
        a1.href = `vendor/${v.id}`;
        a1.style.color = 'black';
        a1.style.textDecoration = 'none';
        a1.className = 'col-sm-2';
        a1.innerHTML = `<strong>${v.username}</strong>`;
        col1.className = 'col-sm-7';
        col1.innerHTML = v.about;
        a.append(img);
        col.append(a);
        row.append(col);
        row.append(a1);
        row.append(col1);
        li.append(row);
        document.querySelector('#ven-ul').append(li);
    })
    document.querySelector('#filter-con').style.display = 'none';
    document.querySelector('#filt').innerHTML = `Filter - ${typ}`;
}

function chooseBtn(btn) {
    document.querySelector('#btn-grp').querySelectorAll('button').forEach(e => e.disabled = false);
    btn.disabled = true;
}

function empty() {
    if (document.querySelector('#srch_inp').value == "")
        return false;
}

function post_items(items) {
    document.querySelector('#list').style.display = 'none';
    document.querySelector('#list1').innerHTML = '';
    items.forEach(item => {
        const cont = document.createElement('div');
        const con = document.createElement('a');
        const vendor = document.createElement('div');
        const price = document.createElement('div');
        const img = document.createElement('img');
        const tag = document.createElement('small');
        const name = document.createElement('h4');
        cont.className = 'col-lg-3 text-center border my-3 mx-4 p-2 hovr';
        cont.id = 'item-cont';
        con.href = `item/${item.id}`;
        con.style.color = 'black';
        img.className = 'img-fluid mw-100 mh-100 d-block mb-2 hov';
        img.src = item.image;
        vendor.className = 'hv';
        vendor.innerHTML = `From: <strong>${item.vendor}</strong>`;
        price.className = 'hv1';
        price.innerHTML = `$<strong>${item.price}</strong>`;
        tag.className = 'bg-warning pl-1 pr-1';
        tag.id = 'tag';
        if (item.upcoming)
            tag.innerHTML = 'Upcoming';
        else tag.innerHTML = 'Instock';
        name.innerHTML = item.name;
        con.append(img);
        con.append(vendor);
        con.append(price);
        cont.append(con);
        cont.append(tag);
        cont.append(name);
        document.querySelector('#list1').append(cont);
    });
}

function post_item(item) {
    document.querySelector('#fill').style.display = 'none';
    const img = document.createElement('img');
    const container = document.createElement('div');
    const text_cont = document.createElement('div');
    const img_cont = document.createElement('div');
    const from = document.createElement('div');
    const name = document.createElement('div');
    const category = document.createElement('div');
    const price = document.createElement('div');
    const description = document.createElement('div');
    const seen_count = document.createElement('div');
    const icb = document.createElement('button');
    const ic = document.createElement('i');
    ic.className = 'fa fa-arrow-left';
    icb.id = 'tag1';
    icb.className = 'btn btn-default';
    icb.append(ic);
    icb.onclick = () => window.location.href = item.vendor_id;
    from.innerHTML = `From: <b>${item.vendor}</b>`;
    name.innerHTML = `Item name: <b>${item.name}</b>`;
    category.innerHTML = `Category: <b>${item.category}</b>`;
    price.innerHTML = `Price: <b>$${item.price}</b>`;
    description.innerHTML = `Description: ${item.description}`;
    seen_count.innerHTML = `Seen: ${item.seen_count} time(s)`;
    img.src = item.image;
    img.style.height = 'auto';
    img.style.width = 'inherit';
    container.className = 'border row mb-4';
    text_cont.className = 'col-sm-5 p-5 txt';
    text_cont.style.position = 'relative';
    img_cont.className = 'col-sm-7';
    img_cont.append(img);
    text_cont.append(name);
    text_cont.append(from);
    text_cont.append(category);
    text_cont.append(price);
    text_cont.append(description);
    text_cont.append(seen_count);
    text_cont.append(icb);
    container.append(text_cont);
    container.append(img_cont);
    document.querySelector('#fill1').append(container);
}

function randomads() {
    document.querySelector('#left').innerHTML = '';
    const h3 = document.createElement('h3');
    h3.innerHTML = 'Ads';
    document.querySelector('#left').append(h3);
    for (let i = 0; i < 3; i++) {
        const img = document.createElement('img');
        img.alt = 'Advertisement image';
        img.className = 'img-fluid mb-3';
        img.src = `https://image.shutterstock.com${ads[Math.floor(Math.random() * ads.length)]}`;
        document.querySelector('#left').append(img);
    }
}