page, article, journal, post, document, messages

cart

/shop/product/<slug>
/shop/brand
/shop/vendor
/shop/pay
/shop/cart
/shop/bookmark

/poll

- date formatting (posted on, modified on)
- pagination : parameterized
- babel select lang html

- blueprint dynamic import

- error page -> 테마/사이트 무관하게 만들 것

- blog theme work


- id: username or email (preferences)
- verify_password function must be overridden.

- 댓글에 댓글 달기
- 댓글 소셜
- 댓글 recaptcha
- 가입 후 댓글달기 기능

- email confirmation
- reset password
- change email address with confirmation

- config/factory pattern refactoring / 블루프린트 로딩 refactoring
- 회원가입 절차 (약관동의/본인인증/정보입력/이메일 인증/가입완료)

validators

- credit card
- cellphone
- local phone
- postal code
- korean registration code

- tag
삭제된 태그를 실제로 테이블에서 삭제 처리할 것
- menu
- attachment management
- history
- dashboard

- sidebar 기능 추가
글보관함 i18n

* Mail
* celery
* Flask-migrate
* Fixtures


상태에 따른 게시물 노출 문제 - 사용자 권한 유무와 같이 처리할 것
공개 게시물만 목록 노출함
게시물 detail 보기는 public 조건 아직 없음
게시물 진짜로 삭제 (erase) 기능 만들 것
카테고리 추가시 '-'를 '&nbsp;'로 변경 할지
sidebar 위젯 방식(MVC)으로 구현
글보관함 i18n

고민 사항 (성능 관련)

- 카테고리 가져올 때 n-join eager-loading (prefetch) 처리 여부
- gravatar 매번 필터로 계산하는 것보다 디비에 저장 여부
- 태그 카운트를 post_tag 테이블에 저장하는 방안
