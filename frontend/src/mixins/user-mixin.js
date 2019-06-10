import { mapActions, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['getUserInfo'])
  },
  methods: {
    ...mapActions(['updateUserInfo'])
  }
}
