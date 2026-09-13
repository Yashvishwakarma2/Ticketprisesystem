const form = document.getElementById("bookingForm");

const quantityInput = document.getElementById("quantity");

const ticketPrice = document.getElementById("ticketPrice");

const totalPrice = document.getElementById("totalPrice");


// Ticket prices

const prices = {
    movie: 150,
    bus: 80,
    train: 120,
    flight: 5000
};


// Get selected ticket

function getSelectedTicket() {

    return document.querySelector(
        'input[name="ticket_type"]:checked'
    ).value;

}


// Update price

function updatePrice() {

    const ticket = getSelectedTicket();

    const quantity =
        parseInt(quantityInput.value) || 1;

    const price = prices[ticket];

    const total = price * quantity;

    ticketPrice.textContent = `₹${price}`;

    totalPrice.textContent = `₹${total}`;
}


// Ticket selection

document
    .querySelectorAll('input[name="ticket_type"]')
    .forEach(input => {

        input.addEventListener(
            "change",
            updatePrice
        );

    });


// Quantity change

quantityInput.addEventListener(
    "input",
    updatePrice
);


// Booking

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const name =
        document.getElementById("name").value;

    const phone =
        document.getElementById("phone").value;

    const ticket_type =
        getSelectedTicket();

    const quantity =
        parseInt(quantityInput.value);


    const response = await fetch("/book", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name,
            phone: phone,
            ticket_type: ticket_type,
            quantity: quantity

        })

    });


    const data = await response.json();


    if (!data.success) {

        alert(data.message);

        return;

    }


    const booking = data.booking;


    document.getElementById(
        "billCard"
    ).style.display = "block";


    document.getElementById(
        "billDetails"
    ).innerHTML = `

        <div class="booking-id">

            <strong>Booking ID</strong>

            <br>

            ${booking.booking_id}

        </div>


        <div class="bill-row">

            <span>Passenger</span>

            <strong>${booking.name}</strong>

        </div>


        <div class="bill-row">

            <span>Phone</span>

            <strong>${booking.phone}</strong>

        </div>


        <div class="bill-row">

            <span>Ticket</span>

            <strong>${booking.ticket}</strong>

        </div>


        <div class="bill-row">

            <span>Price</span>

            <strong>₹${booking.price}</strong>

        </div>


        <div class="bill-row">

            <span>Quantity</span>

            <strong>${booking.quantity}</strong>

        </div>


        <div class="bill-total">

            Total: ₹${booking.total}

        </div>

    `;


    document
        .getElementById("billCard")
        .scrollIntoView({
            behavior: "smooth"
        });

});