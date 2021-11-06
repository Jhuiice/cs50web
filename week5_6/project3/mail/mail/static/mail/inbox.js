document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'))
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener('submit', submit_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

// activates compose view
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


// this function is only called by an event
// therefor the event is passed into the function
// you can alter the event at your will
function submit_email(event){
  // stops the EVENT of the form being posted
  // uses JS instead to POST
  event.preventDefault()

  // add triggers to grab data and send it to django
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  // post email to API route
  fetch('/emails', {
    method:'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })

  .then(load_mailbox('sent'))
}


function load_email(id){
  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {
    // display email here with json api
    console.log(email);

    // show email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // display email
    // Grab the container you will enter information into
    const view = document.querySelector('#email-view');

    view.innerHTML =
    `
    <ul>
      <li class="email-text">Sender: ${email.semder}</li>
      <li class="email-text">Recipient(s) ${email.recipients}</li>
      <li class="email-text">Subject: ${email.subject}</li>
      <li class="email-text">Timestamp: ${email.timestamp}</li>
      <li class="email-text">Body: ${email.body}</li>
    </ul>
    `
    // is there another way around using a try and accept block to change the code?
    try {
      fetch('/emails/' + email.id, {
        method: 'PUT',
        body: JSON.stringify({ read : true})
      })
    }
    catch(err) {
      // do nothing
    }
    finally {
      // do nothing
    }

    // create archive button
    let archive = document.createElement('button');
    // if (email.archive) {
    //   archive.innerHTML = 'Un-Archive'
    // } else {
    //   archive.innerHTML = 'Archive'
    // }

    archive.innerHTML = !email.archive ? 'Archive' : 'Archive';

    archive.className = 'btn btn-sm btn-outline-primary';
    archive.addEventListener('click', () => {
      fetch('/emails/' + email.id, {
        method: 'PUT',
        body: JSON.stringify({ archived: !email.archived})
      })
      .then(response => load_mailbox('inbox'))

    })
    // puts archive message on sent emails
    // How would I go about removing that
    // Comparison of logged in user and sender?
    // How do i get the logged in user with js?
    view.append(archive)


    // create a reply button
    let reply = document.createElement('button')
    reply.innerHTML = "Reply";
    reply.className = 'btn btn-sm btn-outline-primary'

    reply.addEventListener('click', () => {
      compose_email()

      // display recipients and sender and subject
      let sender = email.sender;
      let subject = email.subject;
      let body = email.body;

      body = `On ${email.timestamp} ${email.recipients} wrote: ` + body;

      if (subject.split(" ", 1)[0] != "Re:") {
        subject = "Re: " + subject;
      }

      document.querySelector('#compose-recipients').value = sender;
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = body;
    })
    view.appendChild(reply)
  });

}


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  // document.querySelector('#email-unread-btn').style.display = 'none';

  // Show the mailbox name
  const view = document.querySelector('#emails-view');
  view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    // create div for multiple emails use forEach to create all the divs and then append them to view variable
    emails.forEach(email => {
      let div = document.createElement('div');
      div.style.border = '1px solid black'
      if (!email.read){
        div.style.backgroundColor = 'white';
        console.log('unread')
      }else {
        div.style.backgroundColor = 'gray';
        console.log('read')
      }

      div.className = email['read'] ? "email-list-item-read": "email-list-item-unread";

      // TODO change inner html to fit an appropriate looks
      // this looks ugly
      div.innerHTML =`
          <span class="email-text">Sender: ${email.sender}</span><br>
          <span class="email-text">Subject: ${email.subject}</span><br>
          <span class="email-text">Body: ${email.body}</span><br>
          <span class="email-text">Timestamp: ${email.timestamp}</span><br>
      `;
      // makes the emails clickable and loads the specific email

      div.addEventListener('click', () => load_email(email['id']));
      // to target emails with css
      view.appendChild(div);
    });
  })
}

