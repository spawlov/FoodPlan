$(document).ready(function () {
  const orderForm = $("#order");
  const periodInput = $("#id_period");

  const priceBlock = $('#price')
  const priceWithoutDiscountBlock = $('#without_discount');
  const promoSuccessBlock = $('#promo_success')
  const promoFailBlock = $('#promo_fail')


  const renderPrice = (price, priceWithoutDiscount) => {
    priceWithoutDiscount ? priceWithoutDiscountBlock.text(priceWithoutDiscount) : priceWithoutDiscountBlock.text('');
    priceBlock.text(price);
  }

  const renderSuccessfulPromo = () => {
    promoSuccessBlock.fadeIn()
    promoSuccessBlock.delay(500).fadeOut()
  }

  const renderFailPromo = () => {
    promoFailBlock.fadeIn()
    promoFailBlock.delay(500).fadeOut()
  }

  const submitForm = (success_func) => {
    const data = orderForm.serialize();
    $.ajax({
      type: "GET",
      url: "/get_plan_price/",
      data: data,
      headers: {
        "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val(),
      },
      success: success_func,
      error: function (error) {
        console.error(error);
      },
    });
  }

  const getPrice = () => {
    submitForm((data) => {
      renderPrice(data.price, data.price_without_discount);
    })
  }

  periodInput.change(getPrice);

  $('#apply_promo').click(function(event) {
    event.preventDefault();
    submitForm((data) => {
      const { price, price_without_discount } = data;
      price_without_discount ? renderSuccessfulPromo() : renderFailPromo();
      renderPrice(price, price_without_discount);
    });
  });


  getPrice();
});
