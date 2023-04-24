export default {
  template: `
    <q-chat-message ref="chat_message"
        name="me"
        avatar="https://cdn.quasar.dev/img/avatar1.jpg"
        :text="['hey, how are you?']"
        sent
      />
  `,
  methods: {
  },
  props: {
    sent: Boolean,
    label: String,
    text: String,
    stamp: String,
    name: String,
    avatar: String,
  },
};
