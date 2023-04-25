export default {
  template: `
    <q-chat-message ref="chat_message"
        :name="name"
        :label="label"
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
    text: String,
    stamp: String,
    name: String,
    avatar: String,
    label: String,
  },
};
