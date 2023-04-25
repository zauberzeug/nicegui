export default {
  template: `
    <q-chat-message ref="chat_message"
        :name="name"
        :avatar="avatar"
        :text="[text]"
        :sent=sent
        :stamp="stamp"
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
