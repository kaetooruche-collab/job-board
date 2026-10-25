const SITE = {
  name: 'Yireh Careers',
  tagline: 'Every listing verified. Every link goes to the employer\'s own posting.',
  email: 'yirehcareers@gmail.com',
  whatsapp: '+905338225854',
  whatsappUrl: 'https://wa.me/905338225854',
  goatcounter: 'kayzglobal',
  // Hosted Whop checkout links for the two card-payable packages (Essential, Professional).
  // mode 'off'     : no pay buttons.
  // mode 'sandbox' : buttons only on a page opened with ?pay=test, with a visible TEST banner. Never use for the public site.
  // mode 'live'    : buttons for everyone; URLs must be https://whop.com/checkout/ch_... (a checkout link with the thanks-page redirect; checked by tests and the site monitor).
  checkout: {
    mode: 'off',
    essential: 'https://sandbox.whop.com/checkout/ch_gYh54Svza5zULln',
    professional: 'https://sandbox.whop.com/checkout/ch_ZVTk4UHL8ih0xEn'
  }
};
