function prepare_transaction(public_key, client_secret, return_url, language_code) {
    const stripe = Stripe(public_key, {locale: language_code});
    const options = {
        clientSecret: client_secret,
        appearance: {
            theme: 'night',
            variables: {
                colorPrimary: '#C0ABA7',
                colorBackground: '#342F42',
                colorText: '#E8E2DF',
                colorDanger: '#C2917A',
                fontFamily: 'Tofino Pro, Helvetica, Arial, sans-serif',
                fontSizeBase: '16pt',
                spacingUnit: '2px',
                borderRadius: '10px',
            }
        },
        fonts: [{
            family: 'Tofino Pro',
            src: 'url(fonts/TofinoProPersonal-Regular.otf)',
            weight: '400',
        }]
    };
    const elements = stripe.elements(options);

    const paymentElementOptions = {
        layout: {
            type: 'tabs',
            defaultCollapsed: false,
        }
    }
    const paymentElement = elements.create('payment', paymentElementOptions);
    paymentElement.mount('#payment-element');

    const form = document.getElementById('payment-form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: return_url,
            },
        });

        if (error) {
            // This point will only be reached if there is an immediate error when
            // confirming the payment. Show error to your customer (for example, payment
            // details incomplete)
            const messageContainer = document.querySelector('#error-message');
            messageContainer.textContent = error.message;
        } else {
            // Your customer will be redirected to your `return_url`. For some payment
            // methods like iDEAL, your customer will be redirected to an intermediate
            // site first to authorize the payment, then redirected to the `return_url`.
        }
    });
}