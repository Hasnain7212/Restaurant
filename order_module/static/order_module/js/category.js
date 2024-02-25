document.addEventListener('DOMContentLoaded', function () {
    var cart = [];
    const categoryButtons = document.querySelectorAll('.category-btn');
    const categories = document.querySelectorAll('.category');

    function toggleCategory(category) {
        categories.forEach(function (list) {
            list.style.display = 'none';
        });

        const selectedCategory = document.getElementById(category);
        if (selectedCategory) {
            selectedCategory.style.display = 'block';
        }
    }

    function fetchMenuItems(category) {
        const url = `http://127.0.0.1:8000/order/getitems/${category}/`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const menuItems = data.menu_items;
                updateFrontend(menuItems);
            })
            .catch(error => console.error('Error:', error));
    }

    function updateFrontend(menuItems) {
        const menuList = document.querySelector('.menu-list');
        menuList.innerHTML = '';

        menuItems.forEach(item => {
            const listItem = document.createElement('li');
            listItem.classList.add('menu-item');

            listItem.innerHTML = `
                <form class="item-form">
                    <div class="item-photo">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="item-info">
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                    </div>
                    <div class="item-controls">
                        <span class="item-price">${item.price}</span>
                        <select class="quantity-select">
                            ${item.quantities.map(quantity => `<option value="${quantity}">${quantity}</option>`).join('')}
                        </select>
                    </div>
                    <div class="quantity-controls">
                        <button type="button" class="decrease-quantity">-</button>
                        <span class="quantity">1</span>
                        <button type="button" class="increase-quantity">+</button>
                    </div>
                    <div>
                        <button type="submit" class="add-to-cart">Add to Cart</button>
                        <button type="button" class="remove-from-cart" style="display:none">Remove from Cart</button>
                    </div>
                </form>
            `;

            const form = listItem.querySelector('.item-form');
            const quantitySelect = listItem.querySelector('.quantity-select');
            const quantityDisplay = listItem.querySelector('.quantity');
            const addToCartButton = form.querySelector('.add-to-cart');
            const removeFromCartButton = form.querySelector('.remove-from-cart');

            form.addEventListener('submit', function (event) {
                event.preventDefault();

                const selectedItem = {
                    name: item.name,
                    description: item.description,
                    price: item.price,
                    quantitytype: quantitySelect.value,
                    quantity: parseInt(quantityDisplay.textContent),
                    category: item.category,
                    vegnonveg: item.vegnonveg
                };

                addToCart(selectedItem);
            });

            function addToCart(selectedItem) {

                quantitySelect.disabled = true;

                const existingItem = cart.find(item =>
                    item.name === selectedItem.name &&
                    item.quantitytype === selectedItem.quantitytype &&
                    item.category === selectedItem.category &&
                    item.vegnonveg === selectedItem.vegnonveg
                );

                if (existingItem) {
                    existingItem.quantity += selectedItem.quantity;
                } else {
                    cart.push(selectedItem);
                }

                addToCartButton.style.display = 'none';
                removeFromCartButton.style.display = 'block';

                console.log("aa")

                removeFromCartButton.addEventListener('click', function () {
                    removeFromCart(selectedItem);
                });

                updateTotalBill();
            }

            function removeFromCart(selectedItem) {

                quantitySelect.disabled = false;

                const index = cart.findIndex(cartItem =>
                    cartItem.name === selectedItem.name &&
                    cartItem.quantitytype === selectedItem.quantitytype &&
                    item.category === selectedItem.category &&
                    item.vegnonveg === selectedItem.vegnonveg
                );

                if (index !== -1) {
                    cart.splice(index, 1);

                    addToCartButton.style.display = 'block';
                    removeFromCartButton.style.display = 'none';

                    updateTotalBill();
                }
            }

            function updateQuantityAndCart() {
                const selectedItem = {
                    name: item.name,
                    description: item.description,
                    price: item.price,
                    quantitytype: quantitySelect.value,
                    quantity: parseInt(quantityDisplay.textContent)
                };

                const existingItem = cart.find(item =>
                    item.name === selectedItem.name &&
                    item.quantitytype === selectedItem.quantitytype
                );

                if (existingItem) {
                    existingItem.quantity = selectedItem.quantity;
                    updateTotalBill();
                }
            }

            function updateTotalBill() {
                const buttonContainer = document.querySelector('.button-container');
                if (cart.length === 0) {
                    buttonContainer.style.display = 'none';
                } else {
                    buttonContainer.style.display = 'flex';
                }

                let totalBill = 0;
                const billDetailsElement = document.querySelector('.bill-details');
                billDetailsElement.innerHTML = '';

                document.getElementById("cart_item").value = JSON.stringify(cart);
                
                cart.forEach(item => {
                    const price = parseFloat(item.price);
                    const quantity = parseInt(item.quantity);

                    if (!isNaN(price) && !isNaN(quantity)) {
                        const itemTotal = price * quantity;

                        totalBill += itemTotal;

                        const itemBillDetails = document.createElement('div');
                        itemBillDetails.classList.add('item-bill-details');
                        itemBillDetails.innerHTML = `
                            <span class="item-name">${item.name}(${item.quantitytype})</span>
                            <span class="item-quantity">${quantity}</span>
                            <span class="item-amount">$${itemTotal.toFixed(2)}</span>
                            <button class="remove-item"> X </button>
                        `;

                        billDetailsElement.appendChild(itemBillDetails);

                        const removeButton = itemBillDetails.querySelector('.remove-item');
                        removeButton.addEventListener('click', function () {
                            removeFromCart(item);
                        });
                    } else {
                        console.error(`Invalid price or quantity for item: ${JSON.stringify(item)}`);
                    }
                });
                const billAmountElement = document.querySelector('.bill-amount');
                billAmountElement.textContent = `$${totalBill.toFixed(2)}`;
            }

            const decreaseButton = listItem.querySelector('.decrease-quantity');
            const increaseButton = listItem.querySelector('.increase-quantity');

            decreaseButton.addEventListener('click', function () {
                let currentQuantity = parseInt(quantityDisplay.textContent);
                if (currentQuantity > 1) {
                    currentQuantity--;
                    quantityDisplay.textContent = currentQuantity;
                    updateQuantityAndCart();
                }
            });

            increaseButton.addEventListener('click', function () {
                let currentQuantity = parseInt(quantityDisplay.textContent);
                currentQuantity++;
                quantityDisplay.textContent = currentQuantity;
                updateQuantityAndCart();
            });

            if (item.vegnonveg === 'veg') {
                listItem.classList.add('vegetarian');
            } else if (item.vegnonveg === 'nonveg') {
                listItem.classList.add('non-vegetarian');
            }

            menuList.appendChild(listItem);
        });
    }

    const buttonContainer = document.querySelector('.button-container');
    if (cart.length === 0) {
        buttonContainer.style.display = 'none';
    } else {
        buttonContainer.style.display = 'flex';
    }
    
    categoryButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const category = button.dataset.category;
            toggleCategory(category);
            fetchMenuItems(category);
        });
    });
});
