new TypeIt('#header-title', {
  speed: 50,
  loop: true,
  waitUntilVisible: true
})
.type('We are FOSS@Amrita.<br>')
.pause(300)
.type('A Student Community of Open Source Enthusiasts.')
.pause(300)
.delete(47)
.type('We promote & contribute to Open Source Technologies.')
.pause(300)
.delete(52)
.type('We mentor students to achieve excellence in <br>')
.type('Technical and')
.pause(200)
.delete(13)
.type('Non-Technical Skills.')
.pause(200)
.delete(20)
.delete(46)
.type('The FOSS Club of Amrita Vishwa Vidyapeetham, Amritapuri Campus.')
.pause(300)
.delete(63)
.go();