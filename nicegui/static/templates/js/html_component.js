// {% raw %}


Vue.component('html_component', {

    render: function (h) {
        if (this.jp_props.hasOwnProperty('text')) {
            var comps = [this.jp_props.text];
        } else comps = [];

        for (var i = 0; i < this.jp_props.object_props.length; i++) {
            if (this.jp_props.object_props[i].show) {
                comps.push(h(this.jp_props.object_props[i].vue_type, {
                    props: {
                        jp_props: this.jp_props.object_props[i]
                    }
                }))
            }
        }

        description_object = {
            style: this.jp_props.style,
            attrs: this.jp_props.attrs,
            domProps: {
                // innerHTML: this.jp_props.inner_html
            },
            on: {
                // click: this.eventFunction,
            },
            directives: [],
            slot: this.jp_props.slot,
            ref: 'r' + this.jp_props.id
        };

        if (this.jp_props.classes) {
            description_object['class'] = this.jp_props.classes;
        }

        var event_description = {};
        for (i = 0; i < this.jp_props.events.length; i++) {
            if (!this.jp_props.events[i].includes('__'))
                event_description[this.jp_props.events[i]] = this.eventFunction
        }
        description_object['on'] = event_description;


        if (this.jp_props.inner_html) {
            description_object['domProps'] = {innerHTML: this.jp_props.inner_html};
        }

        return h(this.jp_props.html_tag, description_object, comps);

    },
    data: function () {
        return {
            previous_display: 'none'
        }
    },
    methods: {

        eventFunction: (function (event) {
            if (!this.$props.jp_props.event_propagation) {
                event.stopPropagation();
            }
            if (event.type == 'dragstart') {
                if (this.$props.jp_props.drag_options) {
                    this.$refs['r' + this.$props.jp_props.id].className = this.$props.jp_props.drag_options['drag_classes']
                }
            }
            if (event.type == 'dragover') {
                event.preventDefault();
                return
            }
            if (event.type == 'drop') {

            }
            if (event.type == 'submit') {
                var form_reference = this.$el;
                var props = this.$props;
                event.preventDefault();    //stop form from being submitted in the normal way
                event.stopPropagation();
                var form_elements_list = [];
                var form_elements = form_reference.elements;
                var reader = new FileReader();
                var file_readers = [];
                var reader_ready = [];
                var file_content = [];
                var file_element_position = null;

                for (var i = 0; i < form_elements.length; i++) {
                    var attributes = form_elements[i].attributes;
                    var attr_dict = {};
                    attr_dict['html_tag'] = form_elements[i].tagName.toLowerCase();
                    for (var j = 0; j < attributes.length; j++) {
                        var attr = attributes[j];
                        attr_dict[attr.name] = attr.value;
                        if (attr.name == 'type') {
                            var input_type = attr.value;
                        }
                    }
                    attr_dict['value'] = form_elements[i].value;
                    attr_dict['checked'] = form_elements[i].checked;
                    attr_dict['id'] = form_elements[i].id;

                    if ((attr_dict['html_tag'] == 'input') && (input_type == 'file') && (files_chosen[attr_dict['id']])) {
                        file_element_position = i;
                        reader_ready = [];
                        attr_dict['files'] = [];
                        const file_list = files_chosen[attr_dict['id']];
                        const num_files = file_list.length;
                        for (let j = 0; j < num_files; j++) {
                            reader_ready.push(false);
                            file_content.push('pending');
                            file_readers.push(new FileReader());
                            attr_dict['files'].push({
                                file_content: 'pending',
                                name: file_list[j].name,
                                size: file_list[j].size,
                                type: file_list[j].type,
                                lastModified: file_list[j].lastModified
                            });
                        }
                        for (let j = 0; j < num_files; j++) {
                            file_readers[j].onload = function (e) {
                                file_content[j] = e.target.result.substring(e.target.result.indexOf(",") + 1);
                                reader_ready[j] = true;
                            };
                            file_readers[j].readAsDataURL(file_list[j]);
                        }
                    }

                    form_elements_list.push(attr_dict);
                }

                function check_readers() {
                    if (reader_ready.every(function (x) {
                        return x
                    })) {
                        const file_element = form_elements_list[file_element_position];

                        for (let i = 0; i < file_element.files.length; i++) {
                            file_element.files[i].file_content = file_content[i];
                        }
                        eventHandler(props, event, form_elements_list);
                        return;
                    } else {

                    }
                    setTimeout(check_readers, 300);
                }

                if (file_element_position === null) {
                    eventHandler(props, event, form_elements_list);
                } else {
                    check_readers();
                }

            } else {
                eventHandler(this.$props, event, false);
            }
        }),
        animateFunction: (function () {
            var animation = this.$props.jp_props.animation;
            var element = this.$el;
            element.classList.add('animated', animation);
            element.classList.remove('hidden');
            var event_func = function () {
                element.classList.remove('animated', animation);
                if (animation.includes('Out')) {
                    element.classList.add('hidden');
                } else {
                    // element.classList.remove('hidden');
                }
                element.removeEventListener('animationend', event_func);
            };
            element.addEventListener('animationend', event_func);
        }),
        transitionFunction: (function () {
            let el = this.$refs['r' + this.$props.jp_props.id];
            const props = this.$props.jp_props;
            if (el.$el) el = el.$el;
            const class_list = props.classes.trim().replace(/\s\s+/g, ' ').split(' ');
            // Transition change from hidden to not hidden
            if (props.transition.enter && this.previous_display == 'none' && (!class_list.includes('hidden'))) {

                let enter_list = props.transition.enter.trim().replace(/\s\s+/g, ' ').split(' ');
                let enter_start_list = props.transition.enter_start.trim().replace(/\s\s+/g, ' ').split(' ');
                let enter_end_list = props.transition.enter_end.trim().replace(/\s\s+/g, ' ').split(' ');
                el.classList.add(...enter_start_list);

                setTimeout(function () {
                    el.classList.remove(...enter_start_list);
                    el.classList.add(...enter_list);
                    el.classList.add(...enter_end_list);
                    let event_func = function () {
                        el.removeEventListener('transitionend', event_func);
                        el.classList.remove(...enter_list);
                        el.classList.remove(...enter_end_list);
                    };
                    el.addEventListener('transitionend', event_func);
                }, 3);
            }
            // Transition change from not hidden to hidden
            else if (props.transition.leave && this.previous_display != 'none' && (class_list.includes('hidden'))) {
                let leave_list = props.transition.leave.trim().replace(/\s\s+/g, ' ').split(' ');
                let leave_start_list = props.transition.leave_start.trim().replace(/\s\s+/g, ' ').split(' ');
                let leave_end_list = props.transition.leave_end.trim().replace(/\s\s+/g, ' ').split(' ');
                el.classList.add(...leave_start_list);
                el.classList.remove('hidden');

                setTimeout(function () {
                    el.classList.remove(...leave_start_list);
                    el.classList.add(...leave_list);
                    el.classList.add(...leave_end_list);
                    let event_func = function () {
                        el.removeEventListener('transitionend', event_func);
                        el.classList.remove(...leave_list);
                        el.classList.remove(...leave_end_list);
                        el.classList.add('hidden');

                    };
                    el.addEventListener('transitionend', event_func);
                }, 3);

            }
        }),
        transitionLoadFunction: (function () {
            let el = this.$refs['r' + this.$props.jp_props.id];
            const props = this.$props.jp_props;
            if (el.$el) el = el.$el;
            const class_list = props.classes.trim().replace(/\s\s+/g, ' ').split(' ');


                let load_list = props.transition.load.trim().replace(/\s\s+/g, ' ').split(' ');
                let load_start_list = props.transition.load_start.trim().replace(/\s\s+/g, ' ').split(' ');
                let load_end_list = props.transition.load_end.trim().replace(/\s\s+/g, ' ').split(' ');
                el.classList.add(...load_start_list);

                setTimeout(function () {
                    el.classList.remove(...load_start_list);
                    el.classList.add(...load_list);
                    el.classList.add(...load_end_list);
                    let event_func = function () {
                        el.removeEventListener('transitionend', event_func);
                        el.classList.remove(...load_end_list);
                        el.classList.remove(...load_list);
                    };
                    el.addEventListener('transitionend', event_func);
                }, 3)

        })
    },
    mounted() {
        const el = this.$refs['r' + this.$props.jp_props.id];
        const props = this.$props.jp_props;
         if (Boolean(props.attrs.srcdoc)) {
             this.$props.jp_props.attrs.srcdoc = decodeURIComponent(this.$props.jp_props.attrs.srcdoc);
         }

        if (props.animation) this.animateFunction();
        if (props.id && props.transition && props.transition.load) this.transitionLoadFunction();

        for (let i = 0; i < props.events.length; i++) {
            let split_event = props.events[i].split('__');
            if (split_event[1] == 'out')
                document.addEventListener(split_event[0], function (event) {
                    if (el.contains(event.target)) return;
                    if (el.offsetWidth < 1 && el.offsetHeight < 1) return;
                    e = {
                        'event_type': 'click__out',
                        'id': props.id,
                        'class_name': props.class_name,
                        'html_tag': props.html_tag,
                        'vue_type': props.vue_type,
                        'page_id': page_id,
                        'websocket_id': websocket_id
                    };
                    send_to_server(e, 'event', props.debug);
                });
        }

        if (props.input_type && (props.input_type != 'file')) {
            el.value = props.value;
        }

        if (props.set_focus) {
            this.$nextTick(() => el.focus())
        }


    },
    beforeUpdate() {
        if (this.$props.jp_props.id && this.$props.jp_props.transition) {
            let el = this.$refs['r' + this.$props.jp_props.id];
            if (el.$el) el = el.$el;
            this.previous_display = getComputedStyle(el, null).display;
        }
    },
    updated() {
        const el = this.$refs['r' + this.$props.jp_props.id];
        const props = this.$props.jp_props;
        if (Boolean(props.attrs.srcdoc)) {
             this.$props.jp_props.attrs.srcdoc = decodeURIComponent(this.$props.jp_props.attrs.srcdoc);
         }

        if (props.animation) this.animateFunction();
        if (this.$props.jp_props.id && props.transition) this.transitionFunction();

        if (props.input_type && (props.input_type != 'file')) {

            el.value = props.value;    //make sure that the input value is the correct one received from server

            if (props.input_type == 'radio') {
                if (props.checked) {
                    el.checked = true;  // This un-checks other radio buttons in group also
                } else {
                    el.checked = false;
                }
            }

            if (props.input_type == 'checkbox') {
                el.checked = props.checked;
            }
        }

        if (props.set_focus) {
            this.$nextTick(() => el.focus())
        }

    },
    props: {
        jp_props: Object,

    }
});

// {% endraw %}